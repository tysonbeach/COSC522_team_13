**Feature set:** base (26 features).

**Data:** 75,938 occupants from 34,938 crashes; holdout 15,169 occupants / 6,988 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.769, balanced accuracy 0.746, precision 0.759, recall 0.625, F1 0.685, ROC-AUC 0.834, PR-AUC (AP) 0.798 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.688 vs 0.733; AP 0.544 vs 0.751; depth-4 fatal recall 0.575.

**Top summed importances:** REST_USE, NUMOCCS, AGE, BODY_TYP, TOW_VEH (associations within FARS fatal crashes, not causal effects).
