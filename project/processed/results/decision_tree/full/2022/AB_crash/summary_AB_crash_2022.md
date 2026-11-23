**Feature block:** AB_crash (38 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.806, balanced accuracy 0.789, precision 0.787, recall 0.704, fatal F1 0.743, macro-F1 0.793, ROC-AUC 0.888, PR-AUC (AP) 0.859 (prevalence 0.399).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.754 vs 0.750; AP 0.613 vs 0.794; depth-4 fatal recall 0.578.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, HARM_EV, AGE (associations within FARS fatal crashes, not causal effects).
