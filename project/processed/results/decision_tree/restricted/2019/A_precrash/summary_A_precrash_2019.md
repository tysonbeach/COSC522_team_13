**Feature block:** A_precrash (25 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.741, balanced accuracy 0.654, precision 0.633, recall 0.420, fatal F1 0.505, macro-F1 0.665, ROC-AUC 0.756, PR-AUC (AP) 0.600 (prevalence 0.314).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.607 vs 0.625; AP 0.380 vs 0.541; depth-4 fatal recall 0.341.

**Top summed importances:** REST_USE, AGE, SEAT_POS, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
