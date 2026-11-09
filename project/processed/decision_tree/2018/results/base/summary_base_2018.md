**Feature set:** base (26 features).

**Data:** 70,012 occupants from 31,800 crashes; holdout 13,879 occupants / 6,360 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.767, balanced accuracy 0.743, precision 0.750, recall 0.626, F1 0.683, ROC-AUC 0.827, PR-AUC (AP) 0.787 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.684 vs 0.718; AP 0.536 vs 0.732; depth-4 fatal recall 0.563.

**Top summed importances:** REST_USE, NUMOCCS, AGE, TOW_VEH, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
