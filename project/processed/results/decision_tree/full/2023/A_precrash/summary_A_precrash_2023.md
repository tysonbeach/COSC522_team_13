**Feature block:** A_precrash (25 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.762, balanced accuracy 0.736, precision 0.753, recall 0.605, fatal F1 0.671, macro-F1 0.743, ROC-AUC 0.824, PR-AUC (AP) 0.778 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.675 vs 0.732; AP 0.527 vs 0.727; depth-4 fatal recall 0.621.

**Top summed importances:** REST_USE, PER_TYP, AGE, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
