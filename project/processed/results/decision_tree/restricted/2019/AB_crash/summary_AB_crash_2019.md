**Feature block:** AB_crash (38 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.757, balanced accuracy 0.695, precision 0.637, recall 0.527, fatal F1 0.577, macro-F1 0.703, ROC-AUC 0.808, PR-AUC (AP) 0.651 (prevalence 0.314).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.663 vs 0.644; AP 0.433 vs 0.555; depth-4 fatal recall 0.395.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, BODY_TYP (associations within FARS fatal crashes, not causal effects).
