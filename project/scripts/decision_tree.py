"""Script 3: pre-crash decision tree for one FARS year.

The modeling half of `decision_tree.ipynb` (everything after "Data ready"), unchanged
in method: crash-grouped 80/20 holdout, train-only one-hot/imputation inside a
Pipeline, grouped 5-fold CV, grid search by average precision, one holdout evaluation.

Reads preprocessing.py's cohort and feature list. Every figure is saved as a PNG
(and also shown when run from Jupyter).

Input  (processed/decision_tree/<YEAR>/preprocessing/, from preprocessing.py):
        full_set_filtered_unscaled_<YEAR>.csv
        features_<YEAR>.json
Output (processed/decision_tree/<YEAR>/results/):
        precrash_*.csv, medium_truck_counts_<YEAR>.csv, summary_<YEAR>.md
        figures/*.png

Run from anywhere, e.g. the repo root:  python project/scripts/decision_tree.py 2019
(no year = 2016). From Jupyter, import this file and call main(2019).
"""

import argparse
import json
import platform
import sys
from pathlib import Path

import matplotlib

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    matplotlib.use("Agg")  # no plot windows when run as a plain script
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay,
)
from sklearn.model_selection import (
    GroupShuffleSplit,
    StratifiedGroupKFold,
    GridSearchCV,
    cross_validate,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
DEFAULT_YEAR = 2016
VALID_YEARS = range(2016, 2024)
SEED = 522
N_JOBS = 2
TEST_SIZE = 0.20  # share of crashes held out
N_FOLDS = 5  # grouped CV folds within the training crashes

# Paths are anchored to this file (project/scripts/), so outputs land in project/
# no matter which directory the script is run from.
try:
    PROJECT_DIR = Path(__file__).resolve().parent.parent
except (
    NameError
):  # running cell by cell in Jupyter / VS Code, where __file__ is undefined
    PROJECT_DIR = next(
        p
        for p in (Path.cwd(), Path.cwd().parent, Path.cwd() / "project")
        if (p / "scripts" / "init_load.py").exists()
    )
DECISION_TREE_DIR = PROJECT_DIR / "processed" / "decision_tree"

CRASH_KEY = ["YEAR", "STATE", "ST_CASE"]
PERSON_KEY = CRASH_KEY + ["VEH_NO", "PER_NO"]

# Baseline trees compared before tuning. No class weighting anywhere: fatal is ~40% of
# occupants, so the classes are close to balanced, and weighting mainly shifted the
# fatal/nonfatal cutoff (recall vs precision) while barely changing ROC-AUC/AP. It also
# made the grid search flip between near-tied settings across machines, which breaks
# recall/precision comparisons across years.
BASELINE_PARAMS = {
    "Unrestricted": {},
    "Depth 4": {"max_depth": 4},
}
SCORING = {
    "ap": "average_precision",
    "balanced_accuracy": "balanced_accuracy",
    "roc_auc": "roc_auc",
    "f1": "f1",
}
PARAM_GRID = {
    "tree__max_depth": [4, 8, None],
    "tree__min_samples_leaf": [20, 100],
    "tree__ccp_alpha": [0.0, 0.001],
}
SELECTED_NAME = "Tuned (CV AP)"  # frozen before looking at the holdout

# Medium-truck body types (descriptive count only; NHTSA manual Appendix C).
# Same meaning in every year 2016-2023 and untouched by preprocessing's recodes.
MEDIUM_TRUCK_BODY_TYPES = {60, 61, 62, 64, 67, 71}


# ---------------------------------------------------------------------------
# Command line and output helpers
# ---------------------------------------------------------------------------
def preprocessing_dir(year):
    """processed/decision_tree/<YEAR>/preprocessing/ (written by preprocessing.py)."""
    return DECISION_TREE_DIR / str(year) / "preprocessing"


def output_dir(year):
    """processed/decision_tree/<YEAR>/results/ (this script's outputs)."""
    return DECISION_TREE_DIR / str(year) / "results"


def figure_dir(year):
    return output_dir(year) / "figures"


def parse_year():
    """Year from the command line (DEFAULT_YEAR in Jupyter, which has its own argv)."""
    if INTERACTIVE:
        return DEFAULT_YEAR
    parser = argparse.ArgumentParser(
        description="FARS pre-crash decision tree for one year"
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        default=DEFAULT_YEAR,
        choices=VALID_YEARS,
        metavar="YEAR",
        help="FARS year, 2016-2023 (default: %(default)s)",
    )
    return parser.parse_args().year


def show(df_or_text):
    """display() in notebooks, plain print in scripts."""
    if INTERACTIVE:
        from IPython.display import display

        display(df_or_text)
    else:
        print(
            df_or_text.to_string() if hasattr(df_or_text, "to_string") else df_or_text
        )
        print()


def save_fig(fig, name, year):
    """Save every figure as a PNG; show it only when running interactively."""
    path = figure_dir(year) / f"{name}_{year}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved figure: {path.relative_to(PROJECT_DIR)}")
    plt.show() if INTERACTIVE else plt.close(fig)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def load_inputs(year):
    """preprocessing.py's cohort and feature lists for this year."""
    in_path = preprocessing_dir(year) / f"full_set_filtered_unscaled_{year}.csv"
    features_path = preprocessing_dir(year) / f"features_{year}.json"
    for p in (in_path, features_path):
        if not p.exists():
            raise FileNotFoundError(f"Missing {p}. Run scripts/preprocessing.py first.")
    full_set = pd.read_csv(in_path, low_memory=False)
    features = json.loads(features_path.read_text())
    print(
        f"Loaded {in_path.name}: {full_set.shape[0]:,} rows; "
        f"modeling {len(features['base_features'])} base features"
    )
    return full_set, features


def leakage_cols(features):
    """Columns that must never be model inputs: IDs, label, impact and post-crash."""
    return set(
        features["id_cols"]
        + ["FATAL"]
        + features["impact_cols"]
        + features["post_cols"]
    )


def model_data(full_set, features):
    """Sorted person-level table, features X, label y, and crash group ids."""
    base_features = features["base_features"]
    base_df = full_set[features["id_cols"] + ["FATAL"] + base_features]
    assert not base_df[PERSON_KEY].isna().any().any(), "Missing identity values"
    assert not base_df.duplicated(PERSON_KEY).any(), "Duplicated person records"
    model_df = base_df.sort_values(PERSON_KEY).reset_index(drop=True)
    X = model_df[base_features].copy()
    y = model_df["FATAL"].astype(int)
    groups = pd.Series(
        pd.factorize(pd.MultiIndex.from_frame(model_df[CRASH_KEY]))[0], index=X.index
    )
    assert not (set(X.columns) & leakage_cols(features))
    assert set(y.unique()) == {0, 1}
    return model_df, X, y, groups


# ---------------------------------------------------------------------------
# 1. Reproducible holdout by crash identity
# 80/20 of unique crashes via GroupShuffleSplit(seed 522); everyone in a crash lands on
# the same side. A person-level split manifest is saved for logistic regression to
# reuse.
# ---------------------------------------------------------------------------
def holdout_split(X, y, groups):
    """Crash-grouped train/test split. Returns index arrays for train and test."""
    splitter = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=SEED)
    train_idx, test_idx = next(splitter.split(X, y, groups))
    g_train, g_test = groups.iloc[train_idx], groups.iloc[test_idx]
    assert set(g_train).isdisjoint(set(g_test)), "Crash leakage"
    assert set(y.iloc[train_idx].unique()) == set(y.iloc[test_idx].unique()) == {0, 1}
    return train_idx, test_idx


def save_split_manifest(model_df, test_idx, year):
    manifest = model_df[PERSON_KEY + ["FATAL"]].copy()
    manifest["split"] = "train"
    manifest.loc[test_idx, "split"] = "test"
    manifest.to_csv(
        output_dir(year) / f"precrash_split_{year}_seed{SEED}.csv", index=False
    )


def split_summary(label, target, crash_groups):
    return {
        "split": label,
        "occupants": len(target),
        "crashes": crash_groups.nunique(),
        "nonfatal": int((target == 0).sum()),
        "fatal": int(target.sum()),
        "fatal_share": round(target.mean(), 4),
    }


def library_versions():
    return {
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "matplotlib": matplotlib.__version__,
    }


# ---------------------------------------------------------------------------
# 2. Baselines with train-only preprocessing and grouped CV
# ---------------------------------------------------------------------------
def make_tree(numeric_cols, categorical_cols, **params):
    """Imputation + one-hot encoding (fit on training data only) followed by a tree."""
    preprocess = ColumnTransformer(
        [
            (
                "numeric",
                SimpleImputer(
                    strategy="median", add_indicator=True, keep_empty_features=True
                ),
                numeric_cols,
            ),
            (
                "categorical",
                Pipeline(
                    [
                        (
                            "impute",
                            SimpleImputer(
                                strategy="constant",
                                fill_value=-1,
                                keep_empty_features=True,
                            ),
                        ),
                        (
                            "onehot",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=True),
                        ),
                    ]
                ),
                categorical_cols,
            ),
        ]
    )
    return Pipeline(
        [
            ("preprocess", preprocess),
            ("tree", DecisionTreeClassifier(random_state=SEED, **params)),
        ]
    )


def grouped_cv_splits(X_train, y_train, g_train):
    """Stratified, crash-grouped CV folds within the training data."""
    cv = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    cv_splits = list(cv.split(X_train, y_train, groups=g_train))
    for fit_i, val_i in cv_splits:
        assert set(g_train.iloc[fit_i]).isdisjoint(set(g_train.iloc[val_i]))
    return cv_splits


def baseline_cv(candidates, X_train, y_train, cv_splits):
    """Mean train/CV score (and CV SD) for each baseline tree."""
    cv_rows = []
    for name, model in candidates.items():
        s = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv_splits,
            scoring=SCORING,
            return_train_score=True,
            n_jobs=N_JOBS,
            error_score="raise",
        )
        row = {"model": name}
        for m in SCORING:
            row[f"train_{m}"] = s[f"train_{m}"].mean()
            row[f"cv_{m}"] = s[f"test_{m}"].mean()
            row[f"cv_{m}_sd"] = s[f"test_{m}"].std(ddof=1)
        cv_rows.append(row)
    return pd.DataFrame(cv_rows).set_index("model")


# ---------------------------------------------------------------------------
# 3. Grid search within grouped training CV (selection metric: AP)
# ---------------------------------------------------------------------------
def grid_search(base_model, X_train, y_train, cv_splits):
    search = GridSearchCV(
        base_model,
        PARAM_GRID,
        scoring=SCORING,
        refit="ap",
        cv=cv_splits,
        n_jobs=N_JOBS,
        error_score="raise",
        return_train_score=True,
    )
    search.fit(X_train, y_train)
    return search


# ---------------------------------------------------------------------------
# 4. Final holdout evaluation
# ---------------------------------------------------------------------------
def evaluate(name, model, X_test, y_test):
    """Holdout metrics for one model, plus its predictions and fatal-class scores."""
    pred = model.predict(X_test)
    score = model.predict_proba(X_test)[:, list(model.classes_).index(1)]
    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
    return (
        {
            "model": name,
            "accuracy": accuracy_score(y_test, pred),
            "balanced_accuracy": balanced_accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1": f1_score(y_test, pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, score),
            "pr_auc_ap": average_precision_score(y_test, score),
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "TP": tp,
        },
        pred,
        score,
    )


def evaluate_all(all_models, X_test, y_test):
    rows, predictions, probabilities = [], {}, {}
    for name, model in all_models.items():
        row, predictions[name], probabilities[name] = evaluate(
            name, model, X_test, y_test
        )
        rows.append(row)
    return pd.DataFrame(rows).set_index("model"), predictions, probabilities


def tree_complexity(fitted_models, X_train, y_train):
    return pd.DataFrame(
        [
            {
                "model": n,
                "depth": m.named_steps["tree"].get_depth(),
                "leaves": m.named_steps["tree"].get_n_leaves(),
                "train_accuracy": m.score(X_train, y_train),
            }
            for n, m in fitted_models.items()
        ]
    ).set_index("model")


def plot_confusion_matrices(y_test, predictions, year):
    fig, axes = plt.subplots(1, len(predictions), figsize=(4 * len(predictions), 3.7))
    for ax, name in zip(axes, predictions):
        ConfusionMatrixDisplay.from_predictions(
            y_test,
            predictions[name],
            labels=[0, 1],
            display_labels=["Nonfatal", "Fatal"],
            ax=ax,
            colorbar=False,
            values_format="d",
        )
        ax.set_title(name)
    fig.suptitle(f"Holdout confusion matrices, FARS {year} (rows = actual)")
    fig.tight_layout()
    save_fig(fig, "confusion_matrices", year)


def plot_roc_pr(y_test, probabilities, model_names, year):
    fig, (roc_ax, pr_ax) = plt.subplots(1, 2, figsize=(13, 5))
    for name in model_names:
        RocCurveDisplay.from_predictions(
            y_test, probabilities[name], name=name, ax=roc_ax
        )
        PrecisionRecallDisplay.from_predictions(
            y_test, probabilities[name], name=name, ax=pr_ax
        )
    roc_ax.plot([0, 1], [0, 1], "k--", label="No skill")
    pr_ax.axhline(
        y_test.mean(), color="black", linestyle="--", label="Holdout prevalence"
    )
    roc_ax.legend(fontsize=8)
    pr_ax.legend(fontsize=8)
    roc_ax.set_title("Holdout ROC curves")
    pr_ax.set_title("Holdout precision-recall curves")
    fig.tight_layout()
    save_fig(fig, "roc_pr_curves", year)


# ---------------------------------------------------------------------------
# 5. Tree diagram and feature importances (training data only; not causal)
# ---------------------------------------------------------------------------
def plot_tree_diagram(view_model, year):
    fig, ax = plt.subplots(figsize=(24, 12))
    plot_tree(
        view_model.named_steps["tree"],
        feature_names=view_model.named_steps["preprocess"].get_feature_names_out(),
        class_names=["Nonfatal", "Fatal"],
        filled=True,
        rounded=True,
        proportion=True,
        max_depth=3,
        fontsize=7,
        ax=ax,
    )
    ax.set_title("Depth-4 baseline: first three split levels (training data)")
    fig.tight_layout()
    save_fig(fig, "tree_depth4", year)


def original_field(encoded, base_features):
    """Map an encoded column name (e.g. categorical__BODY_TYP_34.0) to its field."""
    name = encoded.split("__", 1)[1]
    matches = [
        c
        for c in base_features
        if name == c or name.startswith(c + "_") or name == "missingindicator_" + c
    ]
    assert len(matches) == 1, (encoded, matches)
    return matches[0]


def feature_importances(model, base_features):
    """Per-encoded-column importances, and importances summed by original field."""
    feature_names = model.named_steps["preprocess"].get_feature_names_out()
    importances = pd.Series(
        model.named_steps["tree"].feature_importances_,
        index=feature_names,
        name="importance",
    ).sort_values(ascending=False)
    importance_table = importances.rename_axis("encoded_feature").reset_index()
    importance_table["field"] = importance_table["encoded_feature"].map(
        lambda encoded: original_field(encoded, base_features)
    )
    grouped_importance = (
        importance_table.groupby("field")["importance"]
        .sum()
        .sort_values(ascending=False)
    )
    return importances, importance_table, grouped_importance


def plot_importances(importances, grouped_importance, year):
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    importances.head(15).sort_values().plot.barh(ax=axes[0])
    grouped_importance.head(15).sort_values().plot.barh(ax=axes[1])
    axes[0].set_title("Tuned model: encoded-column importance")
    axes[1].set_title("Tuned model: importance summed by original field")
    for ax in axes:
        ax.set_xlabel("Training impurity reduction (not causal)")
    fig.tight_layout()
    save_fig(fig, "feature_importance", year)


# ---------------------------------------------------------------------------
# 6. Medium-truck count (descriptive only; NHTSA manual Appendix C)
# ---------------------------------------------------------------------------
def medium_truck_counts(model_df):
    """Occupants and unique vehicles per medium-truck body type."""
    medium = (
        model_df.loc[model_df["BODY_TYP"].isin(MEDIUM_TRUCK_BODY_TYPES)]
        if "BODY_TYP" in model_df
        else model_df.iloc[0:0]
    )
    truck_audit = (
        medium.groupby("BODY_TYP").size().rename("retained_occupants").to_frame()
    )
    truck_audit["unique_vehicles"] = (
        medium.drop_duplicates(CRASH_KEY + ["VEH_NO"]).groupby("BODY_TYP").size()
    )
    print(
        f"Medium-truck occupants: {len(medium):,}; "
        f"unique vehicles: {len(medium.drop_duplicates(CRASH_KEY + ['VEH_NO'])):,}"
    )
    return truck_audit


# ---------------------------------------------------------------------------
# 7. Run summary (generated from this run's metrics)
# ---------------------------------------------------------------------------
def run_summary(
    y, groups, y_test, g_test, test_results, best_params, grouped_importance
):
    chosen = test_results.loc[SELECTED_NAME]
    unres = test_results.loc["Unrestricted"]
    d4 = test_results.loc["Depth 4"]
    return (
        f"**Data:** {len(y):,} occupants from {groups.nunique():,} crashes; holdout "
        f"{len(y_test):,} "
        f"occupants / {g_test.nunique():,} crashes, no crash overlap.\n\n"
        f"**Tuned tree ({best_params}) on holdout:** accuracy {chosen.accuracy:.3f}, "
        f"balanced accuracy {chosen.balanced_accuracy:.3f}, precision "
        f"{chosen.precision:.3f}, "
        f"recall {chosen.recall:.3f}, F1 {chosen.f1:.3f}, ROC-AUC "
        f"{chosen.roc_auc:.3f}, "
        f"PR-AUC (AP) {chosen.pr_auc_ap:.3f} (prevalence {y_test.mean():.3f}).\n\n"
        "**Baselines:** unrestricted vs depth 4 balanced accuracy "
        f"{unres.balanced_accuracy:.3f} vs "
        f"{d4.balanced_accuracy:.3f}; AP {unres.pr_auc_ap:.3f} vs {d4.pr_auc_ap:.3f}; "
        "depth-4 fatal "
        f"recall {d4.recall:.3f}.\n\n"
        f"**Top summed importances:** {', '.join(grouped_importance.head(5).index)} "
        f"(associations within FARS fatal crashes, not causal effects).\n"
    )


def show_summary(summary):
    if INTERACTIVE:
        from IPython.display import Markdown, display

        display(Markdown(summary))
    else:
        print(summary)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(year=None):
    year = parse_year() if year is None else year
    print(f"FARS year: {year}")
    out_dir = output_dir(year)
    figure_dir(year).mkdir(parents=True, exist_ok=True)

    # Data and holdout split
    full_set, features = load_inputs(year)
    base_features = features["base_features"]
    model_df, X, y, groups = model_data(full_set, features)

    train_idx, test_idx = holdout_split(X, y, groups)
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    g_train, g_test = groups.iloc[train_idx], groups.iloc[test_idx]
    save_split_manifest(model_df, test_idx, year)
    show(
        pd.DataFrame(
            [
                split_summary("train", y_train, g_train),
                split_summary("test", y_test, g_test),
            ]
        ).set_index("split")
    )
    print(library_versions())

    # Baselines
    numeric_cols = [c for c in base_features if c in features["numeric_cols"]]
    categorical_cols = [c for c in base_features if c not in features["numeric_cols"]]
    candidates = {
        name: make_tree(numeric_cols, categorical_cols, **params)
        for name, params in BASELINE_PARAMS.items()
    }
    cv_splits = grouped_cv_splits(X_train, y_train, g_train)
    cv_comparison = baseline_cv(candidates, X_train, y_train, cv_splits)
    cv_comparison.to_csv(out_dir / f"precrash_baseline_cv_{year}.csv")
    show(cv_comparison.round(4))

    # Grid search
    search = grid_search(
        make_tree(numeric_cols, categorical_cols), X_train, y_train, cv_splits
    )
    cv_results = pd.DataFrame(search.cv_results_).sort_values("rank_test_ap")
    cv_results.to_csv(out_dir / f"precrash_cv_{year}.csv", index=False)
    show(
        cv_results[
            [
                "params",
                "mean_train_ap",
                "mean_test_ap",
                "std_test_ap",
                "mean_test_balanced_accuracy",
                "mean_test_roc_auc",
            ]
        ]
        .head(10)
        .round(4)
    )
    print("Best training-CV parameters:", search.best_params_)
    print(f"Best mean CV AP: {search.best_score_:.4f}")

    fitted_models = {
        name: model.fit(X_train, y_train) for name, model in candidates.items()
    }
    fitted_models[SELECTED_NAME] = search.best_estimator_
    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    selected_model = fitted_models[SELECTED_NAME]

    # Holdout evaluation
    all_models = {"Majority dummy": dummy, **fitted_models}
    test_results, predictions, probabilities = evaluate_all(all_models, X_test, y_test)
    test_results.to_csv(out_dir / f"precrash_test_metrics_{year}.csv")
    show(test_results.round(4))
    print(f"Holdout prevalence / no-skill AP reference: {y_test.mean():.4f}")

    complexity = tree_complexity(fitted_models, X_train, y_train)
    complexity.to_csv(out_dir / f"precrash_tree_complexity_{year}.csv")
    show(complexity)

    plot_confusion_matrices(y_test, predictions, year)
    plot_roc_pr(y_test, probabilities, list(fitted_models), year)

    # Tree diagram and importances
    plot_tree_diagram(fitted_models["Depth 4"], year)
    importances, importance_table, grouped_importance = feature_importances(
        selected_model, base_features
    )
    importance_table.to_csv(out_dir / f"precrash_importances_{year}.csv", index=False)
    plot_importances(importances, grouped_importance, year)
    show(grouped_importance.to_frame().round(4))

    # Medium-truck count
    truck_audit = medium_truck_counts(model_df)
    truck_audit.to_csv(out_dir / f"medium_truck_counts_{year}.csv")
    show(truck_audit)

    # Run summary
    summary = run_summary(
        y, groups, y_test, g_test, test_results, search.best_params_, grouped_importance
    )
    (out_dir / f"summary_{year}.md").write_text(summary)
    show_summary(summary)
    assert all(
        not (
            set(m.named_steps["preprocess"].feature_names_in_) & leakage_cols(features)
        )
        for m in fitted_models.values()
    )
    print("Completed. Outputs in", out_dir.relative_to(PROJECT_DIR))


if __name__ == "__main__":
    main()
