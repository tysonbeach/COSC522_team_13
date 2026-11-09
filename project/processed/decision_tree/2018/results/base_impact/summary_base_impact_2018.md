**Feature set:** base_impact (40 features).

**Data:** 70,012 occupants from 31,800 crashes; holdout 13,879 occupants / 6,360 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.805, balanced accuracy 0.786, precision 0.795, recall 0.693, F1 0.740, ROC-AUC 0.885, PR-AUC (AP) 0.862 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.755 vs 0.763; AP 0.614 vs 0.806; depth-4 fatal recall 0.650.

**Top summed importances:** REST_USE, NUMOCCS, PCRASH5, PERNOTMVIT, PERMVIT (associations within FARS fatal crashes, not causal effects).
