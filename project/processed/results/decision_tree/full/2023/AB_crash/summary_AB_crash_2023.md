**Feature block:** AB_crash (38 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.804, balanced accuracy 0.785, precision 0.792, recall 0.692, fatal F1 0.738, macro-F1 0.791, ROC-AUC 0.889, PR-AUC (AP) 0.860 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.750 vs 0.747; AP 0.609 vs 0.790; depth-4 fatal recall 0.553.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, AGE, BODY_TYP (associations within FARS fatal crashes, not causal effects).
