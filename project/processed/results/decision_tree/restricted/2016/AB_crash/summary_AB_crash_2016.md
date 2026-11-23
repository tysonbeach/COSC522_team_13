**Feature block:** AB_crash (38 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.763, balanced accuracy 0.695, precision 0.656, recall 0.513, fatal F1 0.576, macro-F1 0.706, ROC-AUC 0.806, PR-AUC (AP) 0.650 (prevalence 0.314).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.649 vs 0.658; AP 0.419 vs 0.559; depth-4 fatal recall 0.424.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, BODY_TYP (associations within FARS fatal crashes, not causal effects).
