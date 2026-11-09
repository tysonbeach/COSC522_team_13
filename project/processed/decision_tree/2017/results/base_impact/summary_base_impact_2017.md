**Feature set:** base_impact (40 features).

**Data:** 71,957 occupants from 32,435 crashes; holdout 14,578 occupants / 6,487 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.803, balanced accuracy 0.782, precision 0.798, recall 0.678, F1 0.733, ROC-AUC 0.886, PR-AUC (AP) 0.862 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.748 vs 0.764; AP 0.607 vs 0.799; depth-4 fatal recall 0.634.

**Top summed importances:** REST_USE, PERMVIT, NUMOCCS, PCRASH5, PERNOTMVIT (associations within FARS fatal crashes, not causal effects).
