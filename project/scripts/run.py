"""Run the per-year pipeline: preprocess, then the models, for each year.

--mc adds the multicollinearity report between the two. The report only flags related
features; it changes nothing (columns are dropped only via DROP_COLS in
fars/config.py). Stages 1-2 (download, load) are run once, separately.

--models picks the model stages (default: decision_tree only). Random forest and
XGBoost check their split against the decision-tree manifest, so list decision_tree
first (or have run it before) for a year and population. calibration and shap explain
the tuned XGBoost, so they need its results (list xgboost before them, or run it first).

    python project/scripts/run.py full                          every year
    python project/scripts/run.py 2016 2023                     individual years
    python project/scripts/run.py full --mc                     + the multicollinearity report
    python project/scripts/run.py 2019 --block AB_crash         trees for one block only
    python project/scripts/run.py 2016 --models decision_tree random_forest xgboost
    python project/scripts/run.py full --models calibration shap   (after xgboost)
"""

import importlib

import _path  # noqa: F401

from fars import cli, multicollinearity, preprocess

# Model stage -> fars module, imported only when chosen (xgboost is needed only for it).
MODELS = {
    "decision_tree": "decision_tree",
    "random_forest": "random_forest",
    "xgboost": "xgboost_model",
    "calibration": "calibration",
    "shap": "shap_values",
}

if __name__ == "__main__":
    p = cli.parser("Run the per-year pipeline: preprocess, then the models", block=True)
    p.add_argument(
        "--mc",
        action="store_true",
        help="also write the multicollinearity report (report only; changes nothing)",
    )
    p.add_argument(
        "--models",
        nargs="+",
        choices=MODELS,
        default=["decision_tree"],
        help="model stages to run, in order (default: decision_tree)",
    )
    args = cli.parse(p)
    blocks = [args.block] if args.block else None
    stages = [importlib.import_module(f"fars.{MODELS[m]}") for m in args.models]
    for year in args.years:
        preprocess.run(year, args.population)
        if args.mc:
            multicollinearity.run(year, args.population)
        for stage in stages:
            stage.run(year, args.population, blocks)
