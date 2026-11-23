**Feature block:** ABC_post (44 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.828, balanced accuracy 0.819, precision 0.792, recall 0.776, fatal F1 0.784, macro-F1 0.820, ROC-AUC 0.910, PR-AUC (AP) 0.882 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.776 vs 0.805; AP 0.642 vs 0.808; depth-4 fatal recall 0.755.

**Top summed importances:** EJECTION, EXTRICAT, PERMVIT, PCRASH5, AGE (associations within FARS fatal crashes, not causal effects).
