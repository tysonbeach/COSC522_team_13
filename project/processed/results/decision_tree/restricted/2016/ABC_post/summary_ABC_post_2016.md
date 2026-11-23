**Feature block:** ABC_post (44 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.792, balanced accuracy 0.743, precision 0.690, recall 0.611, fatal F1 0.648, macro-F1 0.750, ROC-AUC 0.853, PR-AUC (AP) 0.710 (prevalence 0.314).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.708 vs 0.726; AP 0.483 vs 0.614; depth-4 fatal recall 0.575.

**Top summed importances:** EXTRICAT, EJECTION, AGE, PERMVIT, REST_USE (associations within FARS fatal crashes, not causal effects).
