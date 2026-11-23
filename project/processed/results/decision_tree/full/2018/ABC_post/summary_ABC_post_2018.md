**Feature block:** ABC_post (44 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.828, balanced accuracy 0.818, precision 0.797, recall 0.766, fatal F1 0.781, macro-F1 0.820, ROC-AUC 0.911, PR-AUC (AP) 0.883 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.782 vs 0.788; AP 0.652 vs 0.802; depth-4 fatal recall 0.674.

**Top summed importances:** EJECTION, EXTRICAT, PERMVIT, PCRASH5, AGE (associations within FARS fatal crashes, not causal effects).
