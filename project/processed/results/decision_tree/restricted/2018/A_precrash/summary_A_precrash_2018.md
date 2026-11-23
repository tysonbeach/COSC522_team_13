**Feature block:** A_precrash (25 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.743, balanced accuracy 0.659, precision 0.627, recall 0.434, fatal F1 0.513, macro-F1 0.669, ROC-AUC 0.766, PR-AUC (AP) 0.595 (prevalence 0.311).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.618 vs 0.638; AP 0.387 vs 0.528; depth-4 fatal recall 0.383.

**Top summed importances:** REST_USE, AGE, BODY_TYP, PER_TYP, SEAT_POS (associations within FARS fatal crashes, not causal effects).
