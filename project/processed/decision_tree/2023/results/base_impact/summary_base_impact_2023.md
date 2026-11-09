**Feature set:** base_impact (40 features).

**Data:** 75,938 occupants from 34,938 crashes; holdout 15,169 occupants / 6,988 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.814, balanced accuracy 0.797, precision 0.805, recall 0.710, F1 0.754, ROC-AUC 0.896, PR-AUC (AP) 0.875 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.761 vs 0.758; AP 0.622 vs 0.807; depth-4 fatal recall 0.591.

**Top summed importances:** REST_USE, NUMOCCS, PCRASH5, PERMVIT, PERNOTMVIT (associations within FARS fatal crashes, not causal effects).
