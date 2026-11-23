**Feature block:** AB_crash (38 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.800, balanced accuracy 0.782, precision 0.789, recall 0.691, fatal F1 0.737, macro-F1 0.788, ROC-AUC 0.881, PR-AUC (AP) 0.857 (prevalence 0.406).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.747 vs 0.752; AP 0.611 vs 0.790; depth-4 fatal recall 0.580.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, HARM_EV, AGE (associations within FARS fatal crashes, not causal effects).
