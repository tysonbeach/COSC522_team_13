**Feature block:** ABC_post (44 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.795, balanced accuracy 0.743, precision 0.696, recall 0.606, fatal F1 0.648, macro-F1 0.752, ROC-AUC 0.856, PR-AUC (AP) 0.718 (prevalence 0.311).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.705 vs 0.722; AP 0.478 vs 0.603; depth-4 fatal recall 0.564.

**Top summed importances:** EXTRICAT, EJECTION, AGE, PERMVIT, DEFORMED (associations within FARS fatal crashes, not causal effects).
