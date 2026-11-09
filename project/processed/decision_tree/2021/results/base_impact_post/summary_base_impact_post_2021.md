**Feature set:** base_impact_post (46 features).

**Data:** 79,885 occupants from 36,904 crashes; holdout 16,203 occupants / 7,381 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.833, balanced accuracy 0.824, precision 0.797, recall 0.781, F1 0.789, ROC-AUC 0.919, PR-AUC (AP) 0.897 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.788 vs 0.800; AP 0.655 vs 0.826; depth-4 fatal recall 0.699.

**Top summed importances:** REST_USE, EXTRICAT, NUMOCCS, PCRASH5, PERMVIT (associations within FARS fatal crashes, not causal effects).
