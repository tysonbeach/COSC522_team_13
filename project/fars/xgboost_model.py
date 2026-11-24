"""Stage 7: XGBoost (primary model), one per year and feature block.

The run loop, protocol and outputs are shared with the random forest (ensemble.py);
this module holds only the estimator and its tuning grid. (The module is not named
xgboost.py so that it can never be confused with the xgboost library itself.)

Grid, fixed before looking at any holdout result (8 settings x 5 folds):
    n_estimators {200, 500}; max_depth {3, 6}; learning_rate {0.05, 0.1};
    subsample 0.8 and colsample_bytree 0.8 (fixed).
The default-settings baseline uses XGBoost's defaults (100 rounds, depth 6, rate 0.3).
Every model uses the "hist" tree method, log-loss as the training metric, seed 522,
one core per model (the CV folds already run in parallel), and no class weighting
(no scale_pos_weight; team decision, see decision_tree.py). No early stopping, so
the holdout is never used during fitting.

Outputs: processed/results/xgboost/<POPULATION>/<YEAR>/ (layout in ensemble.py).
"""

import xgboost
from xgboost import XGBClassifier

from . import ensemble
from .config import SEED

MODEL = "xgboost"
PARAM_GRID = {
    "model__n_estimators": [200, 500],
    "model__max_depth": [3, 6],
    "model__learning_rate": [0.05, 0.1],
    "model__subsample": [0.8],
    "model__colsample_bytree": [0.8],
}


def make_xgboost(**params):
    return XGBClassifier(
        tree_method="hist", eval_metric="logloss", random_state=SEED, n_jobs=1, **params
    )


SPEC = ensemble.ModelSpec(
    name=MODEL,
    label="XGBoost",
    make=make_xgboost,
    param_grid=PARAM_GRID,
    importance_note="XGBoost gain importance, training data",
    versions={"xgboost": xgboost.__version__},
)


def run(year, population, blocks=None):
    ensemble.run(SPEC, year, population, blocks)


def main(years, population, blocks=None):
    ensemble.main(SPEC, years, population, blocks)
