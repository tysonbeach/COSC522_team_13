**Feature set:** base_impact (40 features).

**Data:** 78,286 occupants from 36,343 crashes; holdout 15,677 occupants / 7,269 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.810, balanced accuracy 0.795, precision 0.800, recall 0.712, F1 0.753, ROC-AUC 0.893, PR-AUC (AP) 0.873 (prevalence 0.407).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.764 vs 0.774; AP 0.632 vs 0.804; depth-4 fatal recall 0.678.

**Top summed importances:** REST_USE, NUMOCCS, PCRASH5, PERMVIT, PERNOTMVIT (associations within FARS fatal crashes, not causal effects).
