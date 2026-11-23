**Feature block:** ABC_post (44 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.835, balanced accuracy 0.826, precision 0.809, recall 0.776, fatal F1 0.792, macro-F1 0.828, ROC-AUC 0.915, PR-AUC (AP) 0.893 (prevalence 0.406).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.789 vs 0.805; AP 0.662 vs 0.828; depth-4 fatal recall 0.725.

**Top summed importances:** REST_USE, EXTRICAT, PERMVIT, PCRASH5, EJECTION (associations within FARS fatal crashes, not causal effects).
