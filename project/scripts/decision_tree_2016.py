# %% [markdown]
# # Script 3: 2016 decision tree
#
# The modeling half of `decision_tree.ipynb` (everything after "Data ready"), unchanged
# in method: crash-grouped 80/20 holdout, train-only one-hot/imputation inside a
# Pipeline, grouped 5-fold CV, grid search by average precision, one holdout evaluation.
#
# Changes: reads script 2's cohort and feature list, and every figure is saved as a
# PNG in processed/decision_tree/figures/ (and still shown when run as cells).
#
# Input:  processed/decision_tree/full_set_filtered_unscaled_2016.csv
#         processed/decision_tree/features_2016.json
# Output: processed/decision_tree/figures/*.png
#         processed/decision_tree/precrash_*.csv, summary_2016.md
#
# Run from anywhere, e.g. the repo root:  python project/scripts/decision_tree_2016.py

# %%
import json
import platform
import sys
from pathlib import Path

import matplotlib
INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, precision_score,
    recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix,
    ConfusionMatrixDisplay, RocCurveDisplay, PrecisionRecallDisplay)
from sklearn.model_selection import (GroupShuffleSplit, StratifiedGroupKFold,
    GridSearchCV, cross_validate)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree

YEAR = 2016
SEED = 522
N_JOBS = 2

# Paths are anchored to this file (project/scripts/), so outputs land in project/
# no matter which directory the script is run from.
try:
    PROJECT_DIR = Path(__file__).resolve().parent.parent
except NameError:  # running cell by cell in Jupyter / VS Code, where __file__ is undefined
    PROJECT_DIR = next(p for p in (Path.cwd(), Path.cwd().parent, Path.cwd() / "project")
                       if (p / "scripts" / "init_load.py").exists())
RESULT_DIR = PROJECT_DIR / "processed" / "decision_tree"
FIG_DIR = RESULT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def show(df_or_text):
    """display() in notebooks, plain print in scripts."""
    if INTERACTIVE:
        from IPython.display import display
        display(df_or_text)
    else:
        print(df_or_text.to_string() if hasattr(df_or_text, "to_string") else df_or_text)
        print()


def save_fig(fig, name):
    """Save every figure as a PNG; show it only when running interactively."""
    path = FIG_DIR / f"{name}_{YEAR}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved figure: {path.relative_to(PROJECT_DIR)}")
    plt.show() if INTERACTIVE else plt.close(fig)


# %% Load script 2 output
in_path = RESULT_DIR / f"full_set_filtered_unscaled_{YEAR}.csv"
features_path = RESULT_DIR / f"features_{YEAR}.json"
for p in (in_path, features_path):
    if not p.exists():
        raise FileNotFoundError(f"Missing {p}. Run scripts/preprocessing_2016.py first.")
FULL_SET = pd.read_csv(in_path, low_memory=False)
F = json.loads(features_path.read_text())
ID_COLS, BASE_COLS = F["id_cols"], F["base_cols"]
IMPACT_COLS, POST_COLS = F["impact_cols"], F["post_cols"]
NUMERIC_COLS, BASE_FEATURES = F["numeric_cols"], F["base_features"]
print(f"Loaded {in_path.name}: {FULL_SET.shape[0]:,} rows; modeling {len(BASE_FEATURES)} base features")
base_df = FULL_SET[ID_COLS + ["FATAL"] + BASE_FEATURES]

# %% [markdown]
# ## 1. Reproducible holdout by crash identity
# 80/20 of unique crashes via GroupShuffleSplit(seed 522); everyone in a crash lands on
# the same side. A person-level split manifest is saved for logistic regression to reuse.

# %%
CRASH_KEY = ["YEAR", "STATE", "ST_CASE"]
PERSON_KEY = CRASH_KEY + ["VEH_NO", "PER_NO"]
assert not base_df[PERSON_KEY].isna().any().any(), "Missing identity values"
assert not base_df.duplicated(PERSON_KEY).any(), "Duplicated person records"
model_df = base_df.sort_values(PERSON_KEY).reset_index(drop=True)
X = model_df[BASE_FEATURES].copy()
y = model_df["FATAL"].astype(int)
groups = pd.Series(pd.factorize(pd.MultiIndex.from_frame(model_df[CRASH_KEY]))[0], index=X.index)
assert not (set(X.columns) & set(ID_COLS + ["FATAL"] + IMPACT_COLS + POST_COLS))
assert set(y.unique()) == {0, 1}

splitter = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=SEED)
train_idx, test_idx = next(splitter.split(X, y, groups))
X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
g_train, g_test = groups.iloc[train_idx], groups.iloc[test_idx]
assert set(g_train).isdisjoint(set(g_test)), "Crash leakage"
assert set(y_train.unique()) == set(y_test.unique()) == {0, 1}

manifest = model_df[PERSON_KEY + ["FATAL"]].copy()
manifest["split"] = "train"
manifest.loc[test_idx, "split"] = "test"
manifest.to_csv(RESULT_DIR / f"precrash_split_{YEAR}_seed{SEED}.csv", index=False)


def split_summary(label, target, crash_groups):
    return {"split": label, "occupants": len(target), "crashes": crash_groups.nunique(),
            "nonfatal": int((target == 0).sum()), "fatal": int(target.sum()),
            "fatal_share": round(target.mean(), 4)}


show(pd.DataFrame([split_summary("train", y_train, g_train),
                   split_summary("test", y_test, g_test)]).set_index("split"))
print({"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__,
       "sklearn": sklearn.__version__, "matplotlib": matplotlib.__version__})

# %% [markdown]
# ## 2. Baselines with train-only preprocessing and grouped CV

# %%
BASE_NUMERIC = [c for c in BASE_FEATURES if c in NUMERIC_COLS]
BASE_CATEGORICAL = [c for c in BASE_FEATURES if c not in NUMERIC_COLS]


def make_tree(**params):
    preprocess = ColumnTransformer([
        ("numeric", SimpleImputer(strategy="median", add_indicator=True,
                                  keep_empty_features=True), BASE_NUMERIC),
        ("categorical", Pipeline([
            ("impute", SimpleImputer(strategy="constant", fill_value=-1, keep_empty_features=True)),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
        ]), BASE_CATEGORICAL),
    ])
    return Pipeline([("preprocess", preprocess),
                     ("tree", DecisionTreeClassifier(random_state=SEED, **params))])


candidates = {
    "Unrestricted": make_tree(),
    "Depth 4": make_tree(max_depth=4),
    "Depth 4 balanced": make_tree(max_depth=4, class_weight="balanced"),
}
cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
cv_splits = list(cv.split(X_train, y_train, groups=g_train))
for fit_i, val_i in cv_splits:
    assert set(g_train.iloc[fit_i]).isdisjoint(set(g_train.iloc[val_i]))

scoring = {"ap": "average_precision", "balanced_accuracy": "balanced_accuracy",
           "roc_auc": "roc_auc", "f1": "f1"}
cv_rows = []
for name, model in candidates.items():
    s = cross_validate(model, X_train, y_train, cv=cv_splits, scoring=scoring,
                       return_train_score=True, n_jobs=N_JOBS, error_score="raise")
    row = {"model": name}
    for m in scoring:
        row[f"train_{m}"] = s[f"train_{m}"].mean()
        row[f"cv_{m}"] = s[f"test_{m}"].mean()
        row[f"cv_{m}_sd"] = s[f"test_{m}"].std(ddof=1)
    cv_rows.append(row)
cv_comparison = pd.DataFrame(cv_rows).set_index("model")
cv_comparison.to_csv(RESULT_DIR / f"precrash_baseline_cv_{YEAR}.csv")
show(cv_comparison.round(4))

# %% [markdown]
# ## 3. Grid search within grouped training CV (selection metric: AP)

# %%
param_grid = {
    "tree__max_depth": [4, 8, None],
    "tree__min_samples_leaf": [20, 100],
    "tree__ccp_alpha": [0.0, 0.001],
    "tree__class_weight": [None, "balanced"],
}
search = GridSearchCV(make_tree(), param_grid, scoring=scoring, refit="ap", cv=cv_splits,
                      n_jobs=N_JOBS, error_score="raise", return_train_score=True)
search.fit(X_train, y_train)
cv_results = pd.DataFrame(search.cv_results_).sort_values("rank_test_ap")
cv_results.to_csv(RESULT_DIR / f"precrash_cv_{YEAR}.csv", index=False)
show(cv_results[["params", "mean_train_ap", "mean_test_ap", "std_test_ap",
                 "mean_test_balanced_accuracy", "mean_test_roc_auc"]].head(10).round(4))
print("Best training-CV parameters:", search.best_params_)
print(f"Best mean CV AP: {search.best_score_:.4f}")

fitted_models = {name: model.fit(X_train, y_train) for name, model in candidates.items()}
fitted_models["Tuned (CV AP)"] = search.best_estimator_
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
selected_name = "Tuned (CV AP)"   # frozen before looking at the holdout
selected_model = fitted_models[selected_name]

# %% [markdown]
# ## 4. Final holdout evaluation

# %%
def evaluate(name, model):
    pred = model.predict(X_test)
    score = model.predict_proba(X_test)[:, list(model.classes_).index(1)]
    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
    return {"model": name, "accuracy": accuracy_score(y_test, pred),
            "balanced_accuracy": balanced_accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1": f1_score(y_test, pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, score),
            "pr_auc_ap": average_precision_score(y_test, score),
            "TN": tn, "FP": fp, "FN": fn, "TP": tp}, pred, score


all_models = {"Majority dummy": dummy, **fitted_models}
rows, predictions, probabilities = [], {}, {}
for name, model in all_models.items():
    row, predictions[name], probabilities[name] = evaluate(name, model)
    rows.append(row)
test_results = pd.DataFrame(rows).set_index("model")
test_results.to_csv(RESULT_DIR / f"precrash_test_metrics_{YEAR}.csv")
show(test_results.round(4))
print(f"Holdout prevalence / no-skill AP reference: {y_test.mean():.4f}")

complexity = pd.DataFrame([
    {"model": n, "depth": m.named_steps["tree"].get_depth(),
     "leaves": m.named_steps["tree"].get_n_leaves(),
     "train_accuracy": m.score(X_train, y_train)}
    for n, m in fitted_models.items()]).set_index("model")
complexity.to_csv(RESULT_DIR / f"precrash_tree_complexity_{YEAR}.csv")
show(complexity)

fig, axes = plt.subplots(1, len(all_models), figsize=(4 * len(all_models), 3.7))
for ax, name in zip(axes, all_models):
    ConfusionMatrixDisplay.from_predictions(y_test, predictions[name], labels=[0, 1],
        display_labels=["Nonfatal", "Fatal"], ax=ax, colorbar=False, values_format="d")
    ax.set_title(name)
fig.suptitle(f"Holdout confusion matrices, FARS {YEAR} (rows = actual)")
fig.tight_layout()
save_fig(fig, "confusion_matrices")

fig, (roc_ax, pr_ax) = plt.subplots(1, 2, figsize=(13, 5))
for name in fitted_models:
    RocCurveDisplay.from_predictions(y_test, probabilities[name], name=name, ax=roc_ax)
    PrecisionRecallDisplay.from_predictions(y_test, probabilities[name], name=name, ax=pr_ax)
roc_ax.plot([0, 1], [0, 1], "k--", label="No skill")
pr_ax.axhline(y_test.mean(), color="black", linestyle="--", label="Holdout prevalence")
roc_ax.legend(fontsize=8)
pr_ax.legend(fontsize=8)
roc_ax.set_title("Holdout ROC curves")
pr_ax.set_title("Holdout precision-recall curves")
fig.tight_layout()
save_fig(fig, "roc_pr_curves")

# %% [markdown]
# ## 5. Tree diagram and feature importances (training data only; not causal)

# %%
view_model = fitted_models["Depth 4"]
fig, ax = plt.subplots(figsize=(24, 12))
plot_tree(view_model.named_steps["tree"],
          feature_names=view_model.named_steps["preprocess"].get_feature_names_out(),
          class_names=["Nonfatal", "Fatal"], filled=True, rounded=True,
          proportion=True, max_depth=3, fontsize=7, ax=ax)
ax.set_title("Depth-4 baseline: first three split levels (training data)")
fig.tight_layout()
save_fig(fig, "tree_depth4")

feature_names = selected_model.named_steps["preprocess"].get_feature_names_out()
importances = pd.Series(selected_model.named_steps["tree"].feature_importances_,
                        index=feature_names, name="importance").sort_values(ascending=False)


def original_field(encoded):
    name = encoded.split("__", 1)[1]
    matches = [c for c in BASE_FEATURES
               if name == c or name.startswith(c + "_") or name == "missingindicator_" + c]
    assert len(matches) == 1, (encoded, matches)
    return matches[0]


importance_table = importances.rename_axis("encoded_feature").reset_index()
importance_table["field"] = importance_table["encoded_feature"].map(original_field)
grouped_importance = importance_table.groupby("field")["importance"].sum().sort_values(ascending=False)
importance_table.to_csv(RESULT_DIR / f"precrash_importances_{YEAR}.csv", index=False)

fig, axes = plt.subplots(1, 2, figsize=(15, 7))
importances.head(15).sort_values().plot.barh(ax=axes[0])
grouped_importance.head(15).sort_values().plot.barh(ax=axes[1])
axes[0].set_title("Tuned model: encoded-column importance")
axes[1].set_title("Tuned model: importance summed by original field")
for ax in axes:
    ax.set_xlabel("Training impurity reduction (not causal)")
fig.tight_layout()
save_fig(fig, "feature_importance")
show(grouped_importance.to_frame().round(4))

# %% [markdown]
# ## 6. Medium-truck count (descriptive only; NHTSA manual Appendix C)

# %%
MEDIUM_TRUCK_BODY_TYPES = {60, 61, 62, 64, 67, 71}
medium = model_df.loc[model_df["BODY_TYP"].isin(MEDIUM_TRUCK_BODY_TYPES)] \
    if "BODY_TYP" in model_df else model_df.iloc[0:0]
truck_audit = medium.groupby("BODY_TYP").size().rename("retained_occupants").to_frame()
truck_audit["unique_vehicles"] = medium.drop_duplicates(CRASH_KEY + ["VEH_NO"]).groupby("BODY_TYP").size()
truck_audit.to_csv(RESULT_DIR / f"medium_truck_counts_{YEAR}.csv")
print(f"Medium-truck occupants: {len(medium):,}; "
      f"unique vehicles: {len(medium.drop_duplicates(CRASH_KEY + ['VEH_NO'])):,}")
show(truck_audit)

# %% [markdown]
# ## 7. Run summary (generated from this run's metrics)

# %%
chosen, unres = test_results.loc[selected_name], test_results.loc["Unrestricted"]
d4, d4b = test_results.loc["Depth 4"], test_results.loc["Depth 4 balanced"]
summary = (
    f"**Data:** {len(y):,} occupants from {groups.nunique():,} crashes; holdout {len(y_test):,} "
    f"occupants / {g_test.nunique():,} crashes, no crash overlap.\n\n"
    f"**Tuned tree ({search.best_params_}) on holdout:** accuracy {chosen.accuracy:.3f}, "
    f"balanced accuracy {chosen.balanced_accuracy:.3f}, precision {chosen.precision:.3f}, "
    f"recall {chosen.recall:.3f}, F1 {chosen.f1:.3f}, ROC-AUC {chosen.roc_auc:.3f}, "
    f"PR-AUC (AP) {chosen.pr_auc_ap:.3f} (prevalence {y_test.mean():.3f}).\n\n"
    f"**Baselines:** unrestricted vs depth 4 balanced accuracy {unres.balanced_accuracy:.3f} vs "
    f"{d4.balanced_accuracy:.3f}; AP {unres.pr_auc_ap:.3f} vs {d4.pr_auc_ap:.3f}. Depth-4 fatal "
    f"recall with/without balancing {d4b.recall:.3f}/{d4.recall:.3f}.\n\n"
    f"**Top summed importances:** {', '.join(grouped_importance.head(5).index)} "
    f"(associations within FARS fatal crashes, not causal effects).\n"
)
(RESULT_DIR / f"summary_{YEAR}.md").write_text(summary)
if INTERACTIVE:
    from IPython.display import Markdown, display
    display(Markdown(summary))
else:
    print(summary)
assert all(not (set(m.named_steps["preprocess"].feature_names_in_) &
                set(ID_COLS + ["FATAL"] + IMPACT_COLS + POST_COLS))
           for m in fitted_models.values())
print("Completed. Figures in", FIG_DIR.relative_to(PROJECT_DIR))