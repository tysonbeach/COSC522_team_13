"""Stage 5: decision trees, one per year and feature block.

Per block: two untuned baseline trees (unrestricted, depth 4) are cross-validated, a
grid search picks the tuned tree by CV average precision, and all of them plus a
majority-class dummy are scored once on the holdout. The shared protocol (split, CV,
pipeline, metrics) is in modeling.py.

No class weighting: fatal is ~40% of occupants, so the classes are close to balanced.
Weighting mainly shifted the cutoff (recall vs precision) while barely changing
ROC-AUC/AP, and it made the grid search flip between near-tied settings across
machines, which breaks recall/precision comparisons across years.

Outputs (processed/results/decision_tree/<POPULATION>/<YEAR>/):
    holdout_split_<YEAR>_seed522.csv       person-level train/test assignment
    <BLOCK>/  (file names end _<BLOCK>_<YEAR>)
        baseline_cv_*.csv          CV scores of the baseline trees
        grid_search_cv_*.csv       CV scores of every grid setting
        holdout_metrics_*.csv      holdout metrics of every model
        tree_complexity_*.csv      depth and leaves of every tree
        feature_importances_*.csv  tuned tree's importances
        summary_*.md               short written summary
        figures/*.png              confusion matrices, ROC/PR, depth-4 tree, importances
"""

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree

from . import modeling
from .config import BLOCKS, PROJECT_DIR, SEED
from .figures import plt, save_fig
from .paths import block_dir, results_dir

MODEL = "decision_tree"
BASELINES = {"Unrestricted": {}, "Depth 4": {"max_depth": 4}}
PARAM_GRID = {
    "model__max_depth": [4, 8, None],
    "model__min_samples_leaf": [20, 100],
    "model__ccp_alpha": [0.0, 0.001],
}
TUNED = "Tuned (CV AP)"  # name fixed before looking at the holdout


def make_tree(numeric_cols, categorical_cols, **params):
    tree = DecisionTreeClassifier(random_state=SEED, **params)
    return modeling.make_pipeline(tree, numeric_cols, categorical_cols)


def tree_complexity(models, X_train, y_train):
    return pd.DataFrame(
        [
            {
                "model": name,
                "depth": m.named_steps["model"].get_depth(),
                "leaves": m.named_steps["model"].get_n_leaves(),
                "train_accuracy": m.score(X_train, y_train),
            }
            for name, m in models.items()
        ]
    ).set_index("model")


def plot_tree_diagram(pipeline, block):
    """The first three split levels of a fitted tree."""
    fig, ax = plt.subplots(figsize=(24, 12))
    plot_tree(
        pipeline.named_steps["model"],
        feature_names=pipeline.named_steps["preprocess"].get_feature_names_out(),
        class_names=modeling.CLASS_NAMES,
        filled=True,
        rounded=True,
        proportion=True,
        max_depth=3,
        fontsize=7,
        ax=ax,
    )
    ax.set_title(f"Depth-4 baseline (block {block}): first three split levels (training data)")
    fig.tight_layout()
    return fig


def summary_text(data, block, test_results, best_params, by_field):
    tuned, unres, d4 = (test_results.loc[n] for n in [TUNED, "Unrestricted", "Depth 4"])
    y_test = data.y_test
    return (
        f"**Feature block:** {block} ({len(data.features['blocks'][block])} features).\n\n"
        f"**Data:** {len(data.y):,} occupants from {data.groups.nunique():,} crashes; holdout "
        f"{len(y_test):,} occupants / {data.groups.iloc[data.test_idx].nunique():,} crashes, "
        "no crash overlap.\n\n"
        f"**Tuned tree ({best_params}) on holdout:** accuracy {tuned.accuracy:.3f}, "
        f"balanced accuracy {tuned.balanced_accuracy:.3f}, precision {tuned.precision:.3f}, "
        f"recall {tuned.recall:.3f}, fatal F1 {tuned.f1:.3f}, "
        f"macro-F1 {tuned.macro_f1:.3f}, ROC-AUC {tuned.roc_auc:.3f}, "
        f"PR-AUC (AP) {tuned.pr_auc_ap:.3f} (prevalence {y_test.mean():.3f}).\n\n"
        f"**Baselines:** unrestricted vs depth 4 balanced accuracy "
        f"{unres.balanced_accuracy:.3f} vs {d4.balanced_accuracy:.3f}; "
        f"AP {unres.pr_auc_ap:.3f} vs {d4.pr_auc_ap:.3f}; depth-4 fatal recall {d4.recall:.3f}.\n\n"
        f"**Top summed importances:** {', '.join(by_field.head(5).index)} "
        "(associations within FARS fatal crashes, not causal effects).\n"
    )


def run_block(data, block):
    """Baselines, grid search, holdout evaluation and importances for one block."""
    print(f"\n{'-' * 20} FARS {data.year}, block {block} {'-' * 20}")
    out_dir = block_dir(MODEL, data.population, data.year, block)
    fig_dir = out_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    def out(name, ext="csv"):
        return out_dir / f"{name}_{block}_{data.year}.{ext}"

    X_train, X_test = data.X(block)
    y_train, y_test = data.y_train, data.y_test
    modeling.check_no_leakage(data, block, X_train)
    numeric_cols, categorical_cols = data.column_types(block)

    # 1. Untuned baselines, cross-validated
    baselines = {
        name: make_tree(numeric_cols, categorical_cols, **params)
        for name, params in BASELINES.items()
    }
    baseline_cv = modeling.cv_scores(baselines, X_train, y_train, data.cv_splits)
    baseline_cv.to_csv(out("baseline_cv"))
    modeling.show(baseline_cv)

    # 2. Grid search
    search = modeling.grid_search(
        make_tree(numeric_cols, categorical_cols), PARAM_GRID, X_train, y_train, data.cv_splits
    )
    grid = modeling.grid_table(search)
    grid.to_csv(out("grid_search_cv"), index=False)
    shown = [
        "params",
        "mean_train_ap",
        "mean_test_ap",
        "std_test_ap",
        "mean_test_balanced_accuracy",
        "mean_test_roc_auc",
    ]
    modeling.show(grid[shown].head(10))
    print(f"Best CV parameters: {search.best_params_}; mean CV AP {search.best_score_:.4f}")

    # 3. Holdout evaluation
    trees = {name: model.fit(X_train, y_train) for name, model in baselines.items()}
    trees[TUNED] = search.best_estimator_
    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    test_results, predictions, scores = modeling.evaluate(
        {"Majority dummy": dummy, **trees}, X_test, y_test
    )
    test_results.to_csv(out("holdout_metrics"))
    modeling.show(test_results)
    print(f"Holdout prevalence / no-skill AP reference: {y_test.mean():.4f}")

    complexity = tree_complexity(trees, X_train, y_train)
    complexity.to_csv(out("tree_complexity"))
    modeling.show(complexity)

    title = f"Holdout confusion matrices, FARS {data.year}, block {block} (rows = actual)"
    save_fig(
        modeling.plot_confusion_matrices(y_test, predictions, title),
        fig_dir / f"confusion_matrices_{block}_{data.year}.png",
    )
    tree_scores = {name: scores[name] for name in trees}
    save_fig(
        modeling.plot_roc_pr(y_test, tree_scores, block),
        fig_dir / f"roc_pr_curves_{block}_{data.year}.png",
    )

    # 4. Diagram of the depth-4 baseline; importances of the tuned tree
    save_fig(
        plot_tree_diagram(trees["Depth 4"], block), fig_dir / f"tree_depth4_{block}_{data.year}.png"
    )
    importances, by_field = modeling.feature_importances(
        trees[TUNED], data.features["blocks"][block]
    )
    importances.to_csv(out("feature_importances"), index=False)
    save_fig(
        modeling.plot_importances(importances, by_field, f"Tuned tree ({block})"),
        fig_dir / f"feature_importance_{block}_{data.year}.png",
    )
    modeling.show(by_field.to_frame())

    summary = summary_text(data, block, test_results, search.best_params_, by_field)
    out("summary", "md").write_text(summary)
    print(summary)
    print("Outputs in", out_dir.relative_to(PROJECT_DIR))


def run(year, population, blocks=None):
    print(f"\n=== Decision trees {year} ({population} population) ===")
    data = modeling.load_year(year, population)
    out_dir = results_dir(MODEL, population, year)
    out_dir.mkdir(parents=True, exist_ok=True)
    modeling.split_manifest(data).to_csv(
        out_dir / f"holdout_split_{year}_seed{SEED}.csv", index=False
    )
    modeling.show(modeling.split_table(data))
    print(modeling.library_versions())
    for block in blocks or BLOCKS:
        run_block(data, block)


def main(years, population, blocks=None):
    for year in years:
        run(year, population, blocks)
