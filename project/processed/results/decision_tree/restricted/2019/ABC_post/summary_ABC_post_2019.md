**Feature block:** ABC_post (44 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.794, balanced accuracy 0.745, precision 0.695, recall 0.612, fatal F1 0.651, macro-F1 0.753, ROC-AUC 0.848, PR-AUC (AP) 0.723 (prevalence 0.314).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.694 vs 0.700; AP 0.468 vs 0.626; depth-4 fatal recall 0.482.

**Top summed importances:** EXTRICAT, EJECTION, AGE, PERMVIT, REST_USE (associations within FARS fatal crashes, not causal effects).
