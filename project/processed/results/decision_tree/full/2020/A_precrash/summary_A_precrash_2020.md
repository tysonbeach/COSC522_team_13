**Feature block:** A_precrash (25 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.759, balanced accuracy 0.739, precision 0.752, recall 0.623, fatal F1 0.681, macro-F1 0.744, ROC-AUC 0.822, PR-AUC (AP) 0.779 (prevalence 0.413).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.671 vs 0.719; AP 0.536 vs 0.723; depth-4 fatal recall 0.566.

**Top summed importances:** REST_USE, SEAT_POS, AGE, BODY_TYP, RELJCT2 (associations within FARS fatal crashes, not causal effects).
