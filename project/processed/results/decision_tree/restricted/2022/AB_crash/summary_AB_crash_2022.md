**Feature block:** AB_crash (38 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.760, balanced accuracy 0.690, precision 0.650, recall 0.503, fatal F1 0.567, macro-F1 0.701, ROC-AUC 0.806, PR-AUC (AP) 0.642 (prevalence 0.312).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.661 vs 0.649; AP 0.430 vs 0.556; depth-4 fatal recall 0.409.

**Top summed importances:** REST_USE, AGE, PERMVIT, PCRASH5, BODY_TYP (associations within FARS fatal crashes, not causal effects).
