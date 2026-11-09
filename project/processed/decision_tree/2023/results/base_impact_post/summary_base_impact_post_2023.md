**Feature set:** base_impact_post (46 features).

**Data:** 75,938 occupants from 34,938 crashes; holdout 15,169 occupants / 6,988 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.841, balanced accuracy 0.827, precision 0.830, recall 0.759, F1 0.793, ROC-AUC 0.923, PR-AUC (AP) 0.903 (prevalence 0.402).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.795 vs 0.806; AP 0.664 vs 0.833; depth-4 fatal recall 0.731.

**Top summed importances:** REST_USE, EXTRICAT, NUMOCCS, PCRASH5, PERMVIT (associations within FARS fatal crashes, not causal effects).
