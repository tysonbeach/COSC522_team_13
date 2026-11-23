**Feature block:** AB_crash (38 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.796, balanced accuracy 0.779, precision 0.775, recall 0.693, fatal F1 0.732, macro-F1 0.784, ROC-AUC 0.880, PR-AUC (AP) 0.850 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.752 vs 0.765; AP 0.612 vs 0.791; depth-4 fatal recall 0.657.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, HARM_EV, PER_TYP (associations within FARS fatal crashes, not causal effects).
