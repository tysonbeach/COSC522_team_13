**Feature block:** A_precrash (25 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.746, balanced accuracy 0.662, precision 0.638, recall 0.439, fatal F1 0.520, macro-F1 0.673, ROC-AUC 0.770, PR-AUC (AP) 0.597 (prevalence 0.314).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.616 vs 0.633; AP 0.388 vs 0.545; depth-4 fatal recall 0.352.

**Top summed importances:** REST_USE, AGE, PER_TYP, BODY_TYP, SEAT_POS (associations within FARS fatal crashes, not causal effects).
