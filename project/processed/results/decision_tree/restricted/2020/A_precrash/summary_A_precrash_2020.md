**Feature block:** A_precrash (25 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.733, balanced accuracy 0.649, precision 0.611, recall 0.422, fatal F1 0.499, macro-F1 0.659, ROC-AUC 0.757, PR-AUC (AP) 0.588 (prevalence 0.315).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.615 vs 0.623; AP 0.388 vs 0.536; depth-4 fatal recall 0.332.

**Top summed importances:** REST_USE, AGE, BODY_TYP, SEAT_POS, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
