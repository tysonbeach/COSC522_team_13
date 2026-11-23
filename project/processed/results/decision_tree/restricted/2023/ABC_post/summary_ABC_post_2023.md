**Feature block:** ABC_post (44 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.793, balanced accuracy 0.743, precision 0.690, recall 0.611, fatal F1 0.648, macro-F1 0.751, ROC-AUC 0.855, PR-AUC (AP) 0.719 (prevalence 0.312).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.706 vs 0.692; AP 0.481 vs 0.636; depth-4 fatal recall 0.469.

**Top summed importances:** EXTRICAT, EJECTION, AGE, AIR_BAG, PERMVIT (associations within FARS fatal crashes, not causal effects).
