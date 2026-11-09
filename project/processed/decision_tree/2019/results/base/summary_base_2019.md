**Feature set:** base (26 features).

**Data:** 68,910 occupants from 31,371 crashes; holdout 13,856 occupants / 6,275 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.769, balanced accuracy 0.743, precision 0.759, recall 0.615, F1 0.680, ROC-AUC 0.828, PR-AUC (AP) 0.789 (prevalence 0.399).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.691 vs 0.715; AP 0.544 vs 0.726; depth-4 fatal recall 0.532.

**Top summed importances:** REST_USE, NUMOCCS, AGE, VALIGN, TOW_VEH (associations within FARS fatal crashes, not causal effects).
