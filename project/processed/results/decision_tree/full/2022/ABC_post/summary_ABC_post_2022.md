**Feature block:** ABC_post (44 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.831, balanced accuracy 0.818, precision 0.806, recall 0.757, fatal F1 0.781, macro-F1 0.821, ROC-AUC 0.914, PR-AUC (AP) 0.888 (prevalence 0.399).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.790 vs 0.799; AP 0.657 vs 0.822; depth-4 fatal recall 0.716.

**Top summed importances:** REST_USE, EXTRICAT, PERMVIT, PCRASH5, EJECTION (associations within FARS fatal crashes, not causal effects).
