**Data:** 72,525 occupants from 32,698 crashes; holdout 14,661 occupants / 6,540 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__class_weight': 'balanced', 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.762, balanced accuracy 0.753, precision 0.694, recall 0.713, F1 0.704, ROC-AUC 0.831, PR-AUC (AP) 0.792 (prevalence 0.397).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.687 vs 0.725; AP 0.536 vs 0.722. Depth-4 fatal recall with/without balancing 0.649/0.598.

**Top summed importances:** REST_USE, NUMOCCS, AGE, RUR_URB, BODY_TYP (associations within FARS fatal crashes, not causal effects).
