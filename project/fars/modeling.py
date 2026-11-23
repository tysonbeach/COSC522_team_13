"""Model-agnostic pieces shared by every model script (decision tree, RF, XGBoost).

The protocol, the same for every model, year and block:
  1. 80/20 holdout split by crash (GroupShuffleSplit, seed 522): everyone in a crash
     lands on the same side.
  2. 5-fold StratifiedGroupKFold CV within the training crashes.
  3. Imputation and one-hot encoding are fitted inside the pipeline, on training
     folds only.
  4. Model selection by mean CV average precision; the holdout is scored once.
"""

import json
import platform
from dataclasses import dataclass

import matplotlib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    GroupShuffleSplit,
    StratifiedGroupKFold,
    cross_validate,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .config import CRASH_KEY, LABEL, N_JOBS, PERSON_KEY, SEED
from .figures import plt
from .paths import dataset_path, features_path, require

TEST_SIZE = 0.20  # share of crashes held out
N_FOLDS = 5  # grouped CV folds within the training crashes
SCORING = {
    "ap": "average_precision",
    "balanced_accuracy": "balanced_accuracy",
    "roc_auc": "roc_auc",
    "f1": "f1",
}
CLASS_NAMES = ["Nonfatal", "Fatal"]


# ---------------------------------------------------------------------------
# Data and splits (prepared once per year; shared by every block)
# ---------------------------------------------------------------------------
@dataclass
class YearData:
    """One year's occupants with the holdout split and CV folds every block uses."""

    year: int
    population: str
    people: pd.DataFrame  # sorted by PERSON_KEY
    features: dict  # features_<YEAR>.json from preprocess.py
    y: pd.Series
    groups: pd.Series  # crash id per occupant
    train_idx: np.ndarray
    test_idx: np.ndarray
    cv_splits: list  # (fit, validation) index pairs within the training rows

    @property
    def y_train(self):
        return self.y.iloc[self.train_idx]

    @property
    def y_test(self):
        return self.y.iloc[self.test_idx]

    def X(self, block):
        """(X_train, X_test) with only the block's feature columns."""
        X = self.people[self.features["blocks"][block]]
        return X.iloc[self.train_idx], X.iloc[self.test_idx]

    def column_types(self, block):
        """(numeric, categorical) feature columns of the block."""
        cols = self.features["blocks"][block]
        numeric = [c for c in cols if c in self.features["numeric_cols"]]
        return numeric, [c for c in cols if c not in numeric]


def load_year(year, population):
    """Read the year's dataset, then make the crash-grouped holdout split and CV folds."""
    path = require(dataset_path(population, year), "03_preprocess.py")
    features = json.loads(features_path(population, year).read_text())
    people = pd.read_csv(path, low_memory=False)
    assert not people[PERSON_KEY].isna().any().any(), "Missing identity values"
    assert not people.duplicated(PERSON_KEY).any(), "Duplicated person records"
    people = people.sort_values(PERSON_KEY).reset_index(drop=True)
    y = people[LABEL].astype(int)
    assert set(y.unique()) == {0, 1}
    groups = pd.Series(pd.factorize(pd.MultiIndex.from_frame(people[CRASH_KEY]))[0])

    splitter = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=SEED)
    train_idx, test_idx = next(splitter.split(people, y, groups))
    assert set(groups.iloc[train_idx]).isdisjoint(groups.iloc[test_idx]), "Crash leakage"

    y_train, g_train = y.iloc[train_idx], groups.iloc[train_idx]
    cv = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    cv_splits = list(cv.split(people.iloc[train_idx], y_train, groups=g_train))
    for fit_i, val_i in cv_splits:
        assert set(g_train.iloc[fit_i]).isdisjoint(g_train.iloc[val_i]), "CV crash leakage"

    print(f"Loaded {path.name}: {len(people):,} occupants, {groups.nunique():,} crashes")
    return YearData(year, population, people, features, y, groups, train_idx, test_idx, cv_splits)


def split_table(data):
    """Occupants, crashes and fatal share on each side of the holdout split."""
    rows = []
    for name, idx in [("train", data.train_idx), ("test", data.test_idx)]:
        y = data.y.iloc[idx]
        rows.append(
            {
                "split": name,
                "occupants": len(y),
                "crashes": data.groups.iloc[idx].nunique(),
                "nonfatal": int((y == 0).sum()),
                "fatal": int(y.sum()),
                "fatal_share": round(y.mean(), 4),
            }
        )
    return pd.DataFrame(rows).set_index("split")


def split_manifest(data):
    """Person-level record of which side of the holdout each occupant is on."""
    manifest = data.people[PERSON_KEY + [LABEL]].copy()
    manifest["split"] = "train"
    manifest.loc[data.test_idx, "split"] = "test"
    return manifest


def library_versions():
    return {
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "matplotlib": matplotlib.__version__,
    }


def check_no_leakage(data, block, X_train):
    """Model inputs must be exactly the block's features: no IDs, label, or other blocks."""
    assert list(X_train.columns) == data.features["blocks"][block]
    assert not set(X_train.columns) & set(data.features["id_cols"] + [LABEL])


# ---------------------------------------------------------------------------
# Pipeline, cross-validation, tuning
# ---------------------------------------------------------------------------
def make_pipeline(estimator, numeric_cols, categorical_cols):
    """Imputation + one-hot encoding (fit on training data only), then the model.
    Numeric: median + missing-indicator columns. Categorical: NaN -> -1, one-hot."""
    numeric = SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)
    categorical = Pipeline(
        [
            ("impute", SimpleImputer(strategy="constant", fill_value=-1, keep_empty_features=True)),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
        ]
    )
    preprocess = ColumnTransformer(
        [
            ("numeric", numeric, numeric_cols),
            ("categorical", categorical, categorical_cols),
        ]
    )
    return Pipeline([("preprocess", preprocess), ("model", estimator)])


def cv_scores(models, X_train, y_train, cv_splits):
    """Mean train and CV score (and CV SD) of each model, before tuning."""
    rows = []
    for name, model in models.items():
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
        rows.append(row)
    return pd.DataFrame(rows).set_index("model")


def grid_search(pipeline, param_grid, X_train, y_train, cv_splits):
    """Grid search over grouped CV folds, refit on all training data by best mean AP."""
    search = GridSearchCV(
        pipeline,
        param_grid,
        scoring=SCORING,
        refit="ap",
        cv=cv_splits,
        n_jobs=N_JOBS,
        error_score="raise",
        return_train_score=True,
    )
    return search.fit(X_train, y_train)


def grid_table(search):
    return pd.DataFrame(search.cv_results_).sort_values("rank_test_ap")


# ---------------------------------------------------------------------------
# Holdout evaluation
# ---------------------------------------------------------------------------
def evaluate(models, X_test, y_test):
    """Holdout metrics per model, plus each model's predictions and fatal-class scores."""
    rows, predictions, scores = [], {}, {}
    for name, model in models.items():
        pred = model.predict(X_test)
        score = model.predict_proba(X_test)[:, list(model.classes_).index(1)]
        tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
        rows.append(
            {
                "model": name,
                "accuracy": accuracy_score(y_test, pred),
                "balanced_accuracy": balanced_accuracy_score(y_test, pred),
                "precision": precision_score(y_test, pred, zero_division=0),
                "recall": recall_score(y_test, pred, zero_division=0),
                "f1": f1_score(y_test, pred, zero_division=0),
                "macro_f1": f1_score(
                    y_test, pred, labels=[0, 1], average="macro", zero_division=0
                ),
                "roc_auc": roc_auc_score(y_test, score),
                "pr_auc_ap": average_precision_score(y_test, score),
                "TN": tn,
                "FP": fp,
                "FN": fn,
                "TP": tp,
            }
        )
        predictions[name], scores[name] = pred, score
    return pd.DataFrame(rows).set_index("model"), predictions, scores


def plot_confusion_matrices(y_test, predictions, title):
    fig, axes = plt.subplots(1, len(predictions), figsize=(4 * len(predictions), 3.7))
    for ax, (name, pred) in zip(axes, predictions.items()):
        ConfusionMatrixDisplay.from_predictions(
            y_test,
            pred,
            labels=[0, 1],
            display_labels=CLASS_NAMES,
            ax=ax,
            colorbar=False,
            values_format="d",
        )
        ax.set_title(name)
    fig.suptitle(title)
    fig.tight_layout()
    return fig


def plot_roc_pr(y_test, scores, block):
    fig, (roc_ax, pr_ax) = plt.subplots(1, 2, figsize=(13, 5))
    for name, score in scores.items():
        RocCurveDisplay.from_predictions(y_test, score, name=name, ax=roc_ax)
        PrecisionRecallDisplay.from_predictions(y_test, score, name=name, ax=pr_ax)
    roc_ax.plot([0, 1], [0, 1], "k--", label="No skill")
    pr_ax.axhline(y_test.mean(), color="black", linestyle="--", label="Holdout prevalence")
    for ax in (roc_ax, pr_ax):
        ax.legend(fontsize=8)
    roc_ax.set_title(f"Holdout ROC curves (block {block})")
    pr_ax.set_title(f"Holdout precision-recall curves (block {block})")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Feature importance (training data only; associations, not causal effects)
# ---------------------------------------------------------------------------
def original_field(encoded, fields):
    """Map an encoded column name (e.g. categorical__BODY_TYP_34.0) to its field."""
    name = encoded.split("__", 1)[1]
    matches = [
        f
        for f in fields
        if name == f or name.startswith(f + "_") or name == "missingindicator_" + f
    ]
    assert len(matches) == 1, (encoded, matches)
    return matches[0]


def feature_importances(pipeline, fields):
    """Importance per encoded column (with its field), and summed per original field."""
    table = pd.DataFrame(
        {
            "encoded_feature": pipeline.named_steps["preprocess"].get_feature_names_out(),
            "importance": pipeline.named_steps["model"].feature_importances_,
        }
    ).sort_values("importance", ascending=False, ignore_index=True)
    table["field"] = table["encoded_feature"].map(lambda e: original_field(e, fields))
    by_field = table.groupby("field")["importance"].sum().sort_values(ascending=False)
    return table, by_field


def plot_importances(table, by_field, title_prefix, top=15):
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    table.set_index("encoded_feature")["importance"].head(top).sort_values().plot.barh(ax=axes[0])
    by_field.head(top).sort_values().plot.barh(ax=axes[1])
    axes[0].set_title(f"{title_prefix}: encoded-column importance")
    axes[1].set_title(f"{title_prefix}: importance summed by original field")
    for ax in axes:
        ax.set_xlabel("Training impurity reduction (not causal)")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Printing
# ---------------------------------------------------------------------------
def show(table, digits=4):
    print(table.round(digits).to_string() + "\n")
