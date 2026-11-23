**Feature block:** A_precrash (25 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.739, balanced accuracy 0.652, precision 0.618, recall 0.423, fatal F1 0.502, macro-F1 0.663, ROC-AUC 0.759, PR-AUC (AP) 0.591 (prevalence 0.311).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.605 vs 0.630; AP 0.377 vs 0.535; depth-4 fatal recall 0.349.

**Top summed importances:** REST_USE, AGE, SEAT_POS, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
