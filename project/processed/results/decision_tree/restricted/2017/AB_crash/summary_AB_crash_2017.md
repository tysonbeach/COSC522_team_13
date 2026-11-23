**Feature block:** AB_crash (38 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.750, balanced accuracy 0.673, precision 0.631, recall 0.469, fatal F1 0.538, macro-F1 0.683, ROC-AUC 0.796, PR-AUC (AP) 0.637 (prevalence 0.311).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.648 vs 0.643; AP 0.416 vs 0.549; depth-4 fatal recall 0.376.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, BODY_TYP (associations within FARS fatal crashes, not causal effects).
