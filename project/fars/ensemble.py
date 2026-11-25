"""Shared run loop for the tree-ensemble models (random forest, XGBoost).

Same protocol as the decision trees (see modeling.py): the population-specific
crash-grouped 80/20 holdout and 5-fold grouped CV, imputation and one-hot encoding
fitted inside the pipeline, tuning by mean CV average precision, and a single scoring
of the holdout. Before any model is fitted, the year's split is checked against the
decision-tree holdout manifest, so every model family uses the same occupants.

Per block: the model with its library-default settings is cross-validated as a
baseline, a grid search picks the tuned model by mean CV average precision, and the
default, tuned and majority-dummy models are scored once on the holdout.

The encoded features are passed to these models as a dense matrix (ColumnTransformer
sparse_threshold=0). Random forests train several times faster on dense input, and
XGBoost treats entries absent from a sparse matrix as missing, which would turn real
zeros (e.g. AGE 0, a missing-indicator of 0) into "missing". Imputation has already
removed every NaN, so dense input changes no values.

Outputs (processed/results/<MODEL>/<POPULATION>/<YEAR>/):
    holdout_split_<YEAR>_seed522.csv       identical to the decision-tree manifest (checked)
    environment_<YEAR>.json                library versions used for the run
    <BLOCK>/  (file names end _<BLOCK>_<YEAR>)
        baseline_cv_*.csv          CV scores of the default-settings model
        grid_search_cv_*.csv       CV scores of every grid setting
        best_params_*.json         selected setting and its mean CV AP
        holdout_metrics_*.csv      holdout metrics of the dummy, default and tuned models
        feature_importances_*.csv  tuned model's importances
        summary_*.md               short written summary
        figures/*.png              confusion matrices, ROC/PR curves, importances
"""

import json
from dataclasses import dataclass, field
from typing import Callable

import pandas as pd
from sklearn.dummy import DummyClassifier

from . import modeling
from .config import BLOCKS, PROJECT_DIR, SEED
from .figures import save_fig
from .paths import block_dir, results_dir

DEFAULT = "Default settings"
TUNED = "Tuned (CV AP)"  # name fixed before looking at the holdout
REFERENCE_MODEL = "decision_tree"  # its saved split manifest is the reference


@dataclass
class ModelSpec:
    """What differs between ensemble models; everything else is shared."""

    name: str  # results folder, e.g. "random_forest"
    label: str  # display name, e.g. "Random forest"
    make: Callable  # make(**params) -> unfitted estimator
    param_grid: dict  # keys prefixed with "model__", as in decision_tree.PARAM_GRID
    importance_note: str  # what feature_importances_ measures for this model
    versions: dict = field(default_factory=dict)  # extra library versions to record


def make_pipeline(spec, numeric_cols, categorical_cols, **params):
    """modeling.make_pipeline with a dense encoded matrix (see module docstring)."""
    pipeline = modeling.make_pipeline(spec.make(**params), numeric_cols, categorical_cols)
    return pipeline.set_params(preprocess__sparse_threshold=0)


def as_number(value):
    """Some saved decision-tree tables hold numbers as text, e.g. "np.float64(0.74)"."""
    if isinstance(value, str):
        value = value.strip().removeprefix("np.float64(").removesuffix(")")
    return float(value)


def reference_metrics(data, block):
    """The tuned decision tree's holdout row for the same block, if it has been run."""
    path = block_dir(REFERENCE_MODEL, data.population, data.year, block)
    path = path / f"holdout_metrics_{block}_{data.year}.csv"
    if not path.exists():
        return None
    table = pd.read_csv(path, index_col="model")
    return table.loc[TUNED].map(as_number) if TUNED in table.index else None


def summary_text(spec, data, block, test_results, search, by_field):
    tuned, default = test_results.loc[TUNED], test_results.loc[DEFAULT]
    y_test = data.y_test
    tree = reference_metrics(data, block)
    if tree is None:
        tree_line = "not found (run 05_decision_tree.py for this year and population).\n\n"
    else:
        tree_line = (
            f"ROC-AUC {tree.roc_auc:.3f}, PR-AUC (AP) {tree.pr_auc_ap:.3f}, "
            f"balanced accuracy {tree.balanced_accuracy:.3f}, macro-F1 {tree.macro_f1:.3f}.\n\n"
        )
    return (
        f"**Model:** {spec.label}. "
        f"**Feature block:** {block} ({len(data.features['blocks'][block])} features).\n\n"
        f"**Data:** {len(data.y):,} occupants from {data.groups.nunique():,} crashes; holdout "
        f"{len(y_test):,} occupants / {data.groups.iloc[data.test_idx].nunique():,} crashes, "
        "no crash overlap; split identical to the decision-tree manifest.\n\n"
        f"**Tuned model ({search.best_params_}; mean CV AP "
        f"{search.best_score_:.3f}) on holdout:** accuracy {tuned.accuracy:.3f}, "
        f"balanced accuracy {tuned.balanced_accuracy:.3f}, precision {tuned.precision:.3f}, "
        f"recall {tuned.recall:.3f}, fatal F1 {tuned.f1:.3f}, "
        f"macro-F1 {tuned.macro_f1:.3f}, ROC-AUC {tuned.roc_auc:.3f}, "
        f"PR-AUC (AP) {tuned.pr_auc_ap:.3f} (prevalence {y_test.mean():.3f}).\n\n"
        f"**Default settings on holdout:** balanced accuracy {default.balanced_accuracy:.3f}, "
        f"ROC-AUC {default.roc_auc:.3f}, AP {default.pr_auc_ap:.3f}.\n\n"
        f"**Tuned decision tree, same holdout:** {tree_line}"
        f"**Top summed importances:** {', '.join(by_field.head(5).index)} "
        f"({spec.importance_note}; associations within FARS fatal crashes, not causal effects).\n"
    )


def run_block(spec, data, block):
    """Default-settings baseline, grid search, holdout evaluation and importances."""
    print(f"\n{'-' * 20} {spec.label}, FARS {data.year}, block {block} {'-' * 20}")
    out_dir = block_dir(spec.name, data.population, data.year, block)
    fig_dir = out_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    def out(name, ext="csv"):
        return out_dir / f"{name}_{block}_{data.year}.{ext}"

    X_train, X_test = data.X(block)
    y_train, y_test = data.y_train, data.y_test
    modeling.check_no_leakage(data, block, X_train)
    numeric_cols, categorical_cols = data.column_types(block)

    # 1. Library-default settings, cross-validated
    default = {DEFAULT: make_pipeline(spec, numeric_cols, categorical_cols)}
    baseline_cv = modeling.cv_scores(default, X_train, y_train, data.cv_splits)
    baseline_cv.to_csv(out("baseline_cv"))
    modeling.show(baseline_cv)

    # 2. Grid search (selection by mean CV average precision)
    search = modeling.grid_search(
        make_pipeline(spec, numeric_cols, categorical_cols),
        spec.param_grid,
        X_train,
        y_train,
        data.cv_splits,
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
    best = {"best_params": search.best_params_, "mean_cv_ap": search.best_score_}
    out("best_params", "json").write_text(json.dumps(best, indent=2))

    # 3. Holdout evaluation (scored once)
    models = {DEFAULT: default[DEFAULT].fit(X_train, y_train), TUNED: search.best_estimator_}
    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    test_results, predictions, scores = modeling.evaluate(
        {"Majority dummy": dummy, **models}, X_test, y_test
    )
    test_results.to_csv(out("holdout_metrics"))
    modeling.show(test_results)
    print(f"Holdout prevalence / no-skill AP reference: {y_test.mean():.4f}")

    title = f"Holdout confusion matrices, {spec.label}, FARS {data.year}, block {block}"
    save_fig(
        modeling.plot_confusion_matrices(y_test, predictions, title + " (rows = actual)"),
        fig_dir / f"confusion_matrices_{block}_{data.year}.png",
    )
    save_fig(
        modeling.plot_roc_pr(y_test, {name: scores[name] for name in models}, block),
        fig_dir / f"roc_pr_curves_{block}_{data.year}.png",
    )

    # 4. Importances of the tuned model (training data only)
    importances, by_field = modeling.feature_importances(
        models[TUNED], data.features["blocks"][block]
    )
    importances.to_csv(out("feature_importances"), index=False)
    save_fig(
        modeling.plot_importances(importances, by_field, f"Tuned {spec.label} ({block})"),
        fig_dir / f"feature_importance_{block}_{data.year}.png",
    )
    modeling.show(by_field.to_frame())

    summary = summary_text(spec, data, block, test_results, search, by_field)
    out("summary", "md").write_text(summary)
    print(summary)
    print("Outputs in", out_dir.relative_to(PROJECT_DIR))


def run(spec, year, population, blocks=None):
    print(f"\n=== {spec.label} {year} ({population} population) ===")
    data = modeling.load_year(year, population)
    modeling.check_split_matches(data, REFERENCE_MODEL)
    out_dir = results_dir(spec.name, population, year)
    out_dir.mkdir(parents=True, exist_ok=True)
    modeling.split_manifest(data).to_csv(
        out_dir / f"holdout_split_{year}_seed{SEED}.csv", index=False
    )
    versions = {**modeling.library_versions(), **spec.versions}
    (out_dir / f"environment_{year}.json").write_text(json.dumps(versions, indent=2))
    modeling.show(modeling.split_table(data))
    print(versions)
    for block in blocks or BLOCKS:
        run_block(spec, data, block)


def main(spec, years, population, blocks=None):
    for year in years:
        run(spec, year, population, blocks)
