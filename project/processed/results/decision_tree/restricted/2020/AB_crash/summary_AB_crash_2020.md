**Feature block:** AB_crash (38 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.751, balanced accuracy 0.681, precision 0.635, recall 0.493, fatal F1 0.555, macro-F1 0.691, ROC-AUC 0.793, PR-AUC (AP) 0.631 (prevalence 0.315).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.662 vs 0.626; AP 0.432 vs 0.554; depth-4 fatal recall 0.326.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, BODY_TYP (associations within FARS fatal crashes, not causal effects).
