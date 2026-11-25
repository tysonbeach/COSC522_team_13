"""Stage 6: random forests (benchmark), one per year and feature block.

The run loop, protocol and outputs are shared with XGBoost (ensemble.py); this module
holds only the estimator and its tuning grid.

Grid, fixed before looking at any holdout result (6 settings x 5 folds):
    n_estimators 300; max_features {"sqrt", 0.1}; min_samples_leaf {1, 5, 20};
    trees grown to full depth (max_depth None), limited only by min_samples_leaf.
The default-settings baseline uses scikit-learn's defaults (100 trees, "sqrt", leaf 1).
No class weighting (team decision; see decision_tree.py).

Each forest uses one core (n_jobs=1) because the CV folds already run in parallel
(config.N_JOBS); a forest that also used every core would oversubscribe the machine.

Outputs: processed/results/random_forest/<POPULATION>/<YEAR>/ (layout in ensemble.py).
"""

from sklearn.ensemble import RandomForestClassifier

from . import ensemble
from .config import SEED

MODEL = "random_forest"
PARAM_GRID = {
    "model__n_estimators": [300],
    "model__max_features": ["sqrt", 0.1],
    "model__min_samples_leaf": [1, 5, 20],
}


def make_forest(**params):
    return RandomForestClassifier(random_state=SEED, n_jobs=1, **params)


SPEC = ensemble.ModelSpec(
    name=MODEL,
    label="Random forest",
    make=make_forest,
    param_grid=PARAM_GRID,
    importance_note="mean impurity decrease over the trees, training data",
)


def run(year, population, blocks=None):
    ensemble.run(SPEC, year, population, blocks)


def main(years, population, blocks=None):
    ensemble.main(SPEC, years, population, blocks)
