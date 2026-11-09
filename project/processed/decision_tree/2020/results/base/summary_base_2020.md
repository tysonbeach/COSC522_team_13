**Feature set:** base (26 features).

**Data:** 70,447 occupants from 33,199 crashes; holdout 14,138 occupants / 6,640 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.767, balanced accuracy 0.749, precision 0.757, recall 0.643, F1 0.696, ROC-AUC 0.828, PR-AUC (AP) 0.798 (prevalence 0.414).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.690 vs 0.733; AP 0.554 vs 0.749; depth-4 fatal recall 0.600.

**Top summed importances:** REST_USE, NUMOCCS, AGE, BODY_TYP, RUR_URB (associations within FARS fatal crashes, not causal effects).
