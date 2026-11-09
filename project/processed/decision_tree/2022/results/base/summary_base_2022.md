**Feature set:** base (26 features).

**Data:** 78,286 occupants from 36,343 crashes; holdout 15,677 occupants / 7,269 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.770, balanced accuracy 0.750, precision 0.757, recall 0.639, F1 0.693, ROC-AUC 0.833, PR-AUC (AP) 0.803 (prevalence 0.407).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.690 vs 0.739; AP 0.548 vs 0.749; depth-4 fatal recall 0.639.

**Top summed importances:** REST_USE, NUMOCCS, AGE, BODY_TYP, RUR_URB (associations within FARS fatal crashes, not causal effects).
