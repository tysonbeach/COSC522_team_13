"""FARS occupant-survival project: the shared code behind project/scripts/.

Stages, in order (each module has a main(years, ...) that the numbered scripts call):
    download.py           1. raw FARS CSVs                  -> data/
    load.py               2. person + vehicle + crash join  -> processed/joined/
    preprocess.py         3. recodes + cohort               -> processed/datasets/
    multicollinearity.py  4. association report (optional)  -> processed/reports/
    decision_tree.py      5. decision trees                 -> processed/results/decision_tree/
    random_forest.py      6. random forests                 -> processed/results/random_forest/
    xgboost_model.py      7. XGBoost                        -> processed/results/xgboost/
Shared: config.py (settings, columns, blocks), paths.py, recodes.py, cohort.py,
modeling.py (split, CV, pipeline, metrics, plots), ensemble.py (run loop shared by
stages 6-7), figures.py, cli.py.
"""
