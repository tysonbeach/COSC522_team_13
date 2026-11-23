**Feature block:** AB_crash (38 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.754, balanced accuracy 0.685, precision 0.637, recall 0.500, fatal F1 0.560, macro-F1 0.695, ROC-AUC 0.798, PR-AUC (AP) 0.638 (prevalence 0.313).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.660 vs 0.638; AP 0.429 vs 0.545; depth-4 fatal recall 0.365.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, HARM_EV (associations within FARS fatal crashes, not causal effects).
