**Feature block:** AB_crash (38 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.800, balanced accuracy 0.785, precision 0.775, recall 0.708, fatal F1 0.740, macro-F1 0.789, ROC-AUC 0.881, PR-AUC (AP) 0.853 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.745 vs 0.765; AP 0.604 vs 0.798; depth-4 fatal recall 0.664.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, PER_TYP, AGE (associations within FARS fatal crashes, not causal effects).
