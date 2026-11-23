**Feature block:** AB_crash (38 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.797, balanced accuracy 0.784, precision 0.779, recall 0.710, fatal F1 0.743, macro-F1 0.787, ROC-AUC 0.883, PR-AUC (AP) 0.863 (prevalence 0.413).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.748 vs 0.765; AP 0.618 vs 0.797; depth-4 fatal recall 0.648.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, HARM_EV, AGE (associations within FARS fatal crashes, not causal effects).
