**Feature block:** ABC_post (44 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.796, balanced accuracy 0.748, precision 0.694, recall 0.620, fatal F1 0.655, macro-F1 0.755, ROC-AUC 0.854, PR-AUC (AP) 0.717 (prevalence 0.312).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.699 vs 0.711; AP 0.472 vs 0.623; depth-4 fatal recall 0.531.

**Top summed importances:** EXTRICAT, EJECTION, AGE, AIR_BAG, PERMVIT (associations within FARS fatal crashes, not causal effects).
