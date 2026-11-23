**Feature block:** ABC_post (44 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.798, balanced accuracy 0.751, precision 0.699, recall 0.625, fatal F1 0.660, macro-F1 0.758, ROC-AUC 0.860, PR-AUC (AP) 0.723 (prevalence 0.313).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.706 vs 0.695; AP 0.479 vs 0.641; depth-4 fatal recall 0.468.

**Top summed importances:** EXTRICAT, EJECTION, AGE, PERMVIT, AIR_BAG (associations within FARS fatal crashes, not causal effects).
