**Feature block:** AB_crash (38 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.802, balanced accuracy 0.783, precision 0.785, recall 0.692, fatal F1 0.736, macro-F1 0.789, ROC-AUC 0.881, PR-AUC (AP) 0.853 (prevalence 0.398).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.745 vs 0.760; AP 0.601 vs 0.782; depth-4 fatal recall 0.610.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, AGE, HARM_EV (associations within FARS fatal crashes, not causal effects).
