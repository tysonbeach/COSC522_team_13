**Feature block:** A_precrash (25 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.736, balanced accuracy 0.650, precision 0.612, recall 0.423, fatal F1 0.500, macro-F1 0.660, ROC-AUC 0.761, PR-AUC (AP) 0.592 (prevalence 0.313).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.599 vs 0.623; AP 0.373 vs 0.546; depth-4 fatal recall 0.321.

**Top summed importances:** REST_USE, AGE, BODY_TYP, SEAT_POS, PER_TYP (associations within FARS fatal crashes, not causal effects).
