**Feature block:** ABC_post (44 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.834, balanced accuracy 0.826, precision 0.809, recall 0.782, fatal F1 0.795, macro-F1 0.828, ROC-AUC 0.917, PR-AUC (AP) 0.895 (prevalence 0.413).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.785 vs 0.809; AP 0.664 vs 0.833; depth-4 fatal recall 0.742.

**Top summed importances:** REST_USE, EXTRICAT, PERMVIT, PCRASH5, EJECTION (associations within FARS fatal crashes, not causal effects).
