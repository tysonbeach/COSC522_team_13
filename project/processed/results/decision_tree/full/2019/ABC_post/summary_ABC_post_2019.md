**Feature block:** ABC_post (44 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.828, balanced accuracy 0.817, precision 0.792, recall 0.764, fatal F1 0.778, macro-F1 0.819, ROC-AUC 0.911, PR-AUC (AP) 0.881 (prevalence 0.394).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.775 vs 0.795; AP 0.634 vs 0.814; depth-4 fatal recall 0.713.

**Top summed importances:** REST_USE, EXTRICAT, PERMVIT, PCRASH5, AGE (associations within FARS fatal crashes, not causal effects).
