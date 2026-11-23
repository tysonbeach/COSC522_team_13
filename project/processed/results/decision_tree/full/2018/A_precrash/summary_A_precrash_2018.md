**Feature block:** A_precrash (25 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.757, balanced accuracy 0.733, precision 0.738, recall 0.611, fatal F1 0.669, macro-F1 0.738, ROC-AUC 0.815, PR-AUC (AP) 0.761 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.668 vs 0.713; AP 0.522 vs 0.710; depth-4 fatal recall 0.523.

**Top summed importances:** REST_USE, PER_TYP, AGE, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
