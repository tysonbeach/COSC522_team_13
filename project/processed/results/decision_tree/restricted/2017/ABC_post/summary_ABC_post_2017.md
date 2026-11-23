**Feature block:** ABC_post (44 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.791, balanced accuracy 0.745, precision 0.680, recall 0.621, fatal F1 0.649, macro-F1 0.750, ROC-AUC 0.852, PR-AUC (AP) 0.713 (prevalence 0.311).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.698 vs 0.703; AP 0.469 vs 0.580; depth-4 fatal recall 0.506.

**Top summed importances:** EXTRICAT, EJECTION, AGE, PERMVIT, DEFORMED (associations within FARS fatal crashes, not causal effects).
