**Feature block:** A_precrash (25 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.738, balanced accuracy 0.648, precision 0.623, recall 0.408, fatal F1 0.493, macro-F1 0.658, ROC-AUC 0.758, PR-AUC (AP) 0.584 (prevalence 0.312).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.611 vs 0.641; AP 0.382 vs 0.526; depth-4 fatal recall 0.408.

**Top summed importances:** REST_USE, AGE, SEAT_POS, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
