**Feature block:** AB_crash (38 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.753, balanced accuracy 0.681, precision 0.635, recall 0.490, fatal F1 0.553, macro-F1 0.691, ROC-AUC 0.797, PR-AUC (AP) 0.633 (prevalence 0.312).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.655 vs 0.620; AP 0.422 vs 0.540; depth-4 fatal recall 0.304.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, HARM_EV (associations within FARS fatal crashes, not causal effects).
