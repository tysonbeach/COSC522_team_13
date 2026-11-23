**Feature block:** A_precrash (25 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.756, balanced accuracy 0.734, precision 0.734, recall 0.618, fatal F1 0.671, macro-F1 0.739, ROC-AUC 0.817, PR-AUC (AP) 0.760 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.677 vs 0.720; AP 0.531 vs 0.712; depth-4 fatal recall 0.564.

**Top summed importances:** REST_USE, PER_TYP, AGE, BODY_TYP, SEAT_POS (associations within FARS fatal crashes, not causal effects).
