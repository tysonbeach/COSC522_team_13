**Feature block:** AB_crash (38 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.764, balanced accuracy 0.697, precision 0.652, recall 0.520, fatal F1 0.578, macro-F1 0.707, ROC-AUC 0.813, PR-AUC (AP) 0.654 (prevalence 0.311).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.663 vs 0.638; AP 0.429 vs 0.556; depth-4 fatal recall 0.350.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, HARM_EV (associations within FARS fatal crashes, not causal effects).
