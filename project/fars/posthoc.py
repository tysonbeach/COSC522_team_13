"""Shared set-up for the post-hoc analyses of the tuned XGBoost (stages 8-9).

Fitted models are not saved (size), so calibration (calibration.py) and SHAP
(shap_values.py) refit the tuned XGBoost from its saved best_params_<BLOCK>_<YEAR>.json
on exactly the same training rows: the same population-specific dataset, crash-grouped
holdout and CV folds as stages 5-7. Before anything is refitted, the year's split is
checked against both the decision-tree and the XGBoost manifests.

The refit is then scored on the holdout and compared with the saved tuned-XGBoost
holdout metrics. On the machine and library versions that produced the saved results
the two agree; on another platform the row/column subsampling can differ slightly
(the Nov 23 log saw holdout AP move by up to about 0.004), so a difference is
reported in refit_check_<YEAR>.csv and printed, not treated as an error.
"""

import json

import pandas as pd

from . import ensemble, modeling
from .paths import block_dir, require
from .xgboost_model import SPEC

SOURCE = SPEC.name  # the model the analyses explain ("xgboost")
REPRODUCED_TOL = 1e-6  # |refit AP - saved AP| at or below this counts as reproduced


def load_checked(year, population):
    """The year's data, with its split checked against the tree and XGBoost manifests."""
    data = modeling.load_year(year, population)
    modeling.check_split_matches(data, ensemble.REFERENCE_MODEL)
    modeling.check_split_matches(data, SOURCE)
    return data


def best_params(data, block):
    path = block_dir(SOURCE, data.population, data.year, block)
    path = require(path / f"best_params_{block}_{data.year}.json", "07_xgboost.py")
    return json.loads(path.read_text())["best_params"]


def unprefixed(params):
    """{"model__max_depth": 6} -> {"max_depth": 6}, for building the estimator directly."""
    return {k.removeprefix("model__"): v for k, v in params.items()}


def make_tuned(data, block):
    """Unfitted pipeline with the saved tuned XGBoost settings."""
    numeric_cols, categorical_cols = data.column_types(block)
    params = unprefixed(best_params(data, block))
    return ensemble.make_pipeline(SPEC, numeric_cols, categorical_cols, **params)


def refit_tuned(data, block):
    """Fit the tuned XGBoost on the training rows; returns the pipeline and its check row."""
    X_train, X_test = data.X(block)
    modeling.check_no_leakage(data, block, X_train)
    model = make_tuned(data, block).fit(X_train, data.y_train)
    metrics, _, _ = modeling.evaluate({ensemble.TUNED: model}, X_test, data.y_test)
    refit = metrics.loc[ensemble.TUNED]

    path = block_dir(SOURCE, data.population, data.year, block)
    path = require(path / f"holdout_metrics_{block}_{data.year}.csv", "07_xgboost.py")
    saved = pd.read_csv(path, index_col="model").loc[ensemble.TUNED].map(ensemble.as_number)
    check = {
        "block": block,
        "params": json.dumps(best_params(data, block), sort_keys=True),
        "saved_roc_auc": saved.roc_auc,
        "refit_roc_auc": refit.roc_auc,
        "saved_ap": saved.pr_auc_ap,
        "refit_ap": refit.pr_auc_ap,
        "ap_difference": refit.pr_auc_ap - saved.pr_auc_ap,
        "same_confusion_counts": all(
            int(saved[c]) == int(refit[c]) for c in ["TN", "FP", "FN", "TP"]
        ),
    }
    check["reproduced"] = (
        abs(check["ap_difference"]) <= REPRODUCED_TOL and check["same_confusion_counts"]
    )
    note = "reproduced" if check["reproduced"] else "NOT identical (see refit_check)"
    print(
        f"Refit tuned XGBoost ({block}): holdout AP {refit.pr_auc_ap:.4f} vs saved "
        f"{saved.pr_auc_ap:.4f} -> {note}"
    )
    return model, check


def save_refit_checks(checks, out_dir, year):
    out_dir.mkdir(parents=True, exist_ok=True)
    table = pd.DataFrame(checks)
    path = out_dir / f"refit_check_{year}.csv"
    if path.exists():  # keep rows of blocks not rerun this time (e.g. --block)
        old = pd.read_csv(path)
        table = pd.concat([old[~old.block.isin(table.block)], table], ignore_index=True)
    table.to_csv(path, index=False)
    return table


def environment(out_dir, year):
    versions = {**modeling.library_versions(), **SPEC.versions}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"environment_{year}.json").write_text(json.dumps(versions, indent=2))
    return versions
