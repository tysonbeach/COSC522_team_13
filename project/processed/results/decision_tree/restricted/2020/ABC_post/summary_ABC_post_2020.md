**Feature block:** ABC_post (44 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.797, balanced accuracy 0.752, precision 0.696, recall 0.631, fatal F1 0.662, macro-F1 0.759, ROC-AUC 0.853, PR-AUC (AP) 0.717 (prevalence 0.315).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.700 vs 0.725; AP 0.476 vs 0.631; depth-4 fatal recall 0.579.

**Top summed importances:** EXTRICAT, EJECTION, AGE, AIR_BAG, REST_USE (associations within FARS fatal crashes, not causal effects).
