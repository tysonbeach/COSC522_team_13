**Feature block:** A_precrash (25 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.758, balanced accuracy 0.732, precision 0.736, recall 0.610, fatal F1 0.667, macro-F1 0.738, ROC-AUC 0.817, PR-AUC (AP) 0.766 (prevalence 0.398).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.676 vs 0.720; AP 0.527 vs 0.708; depth-4 fatal recall 0.561.

**Top summed importances:** REST_USE, SEAT_POS, AGE, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
