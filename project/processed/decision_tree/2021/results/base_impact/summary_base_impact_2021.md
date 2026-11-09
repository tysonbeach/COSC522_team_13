**Feature set:** base_impact (40 features).

**Data:** 79,885 occupants from 36,904 crashes; holdout 16,203 occupants / 7,381 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.807, balanced accuracy 0.789, precision 0.791, recall 0.701, F1 0.744, ROC-AUC 0.888, PR-AUC (AP) 0.864 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.756 vs 0.755; AP 0.617 vs 0.793; depth-4 fatal recall 0.611.

**Top summed importances:** REST_USE, NUMOCCS, PERMVIT, PCRASH5, PERNOTMVIT (associations within FARS fatal crashes, not causal effects).
