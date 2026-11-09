**Feature set:** base_impact_post (46 features).

**Data:** 70,012 occupants from 31,800 crashes; holdout 13,879 occupants / 6,360 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.831, balanced accuracy 0.819, precision 0.809, recall 0.757, F1 0.782, ROC-AUC 0.914, PR-AUC (AP) 0.891 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.784 vs 0.794; AP 0.651 vs 0.823; depth-4 fatal recall 0.681.

**Top summed importances:** REST_USE, EXTRICAT, NUMOCCS, PCRASH5, PERMVIT (associations within FARS fatal crashes, not causal effects).
