**Feature set:** base_impact_post (46 features).

**Data:** 78,286 occupants from 36,343 crashes; holdout 15,677 occupants / 7,269 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.833, balanced accuracy 0.822, precision 0.819, recall 0.758, F1 0.787, ROC-AUC 0.916, PR-AUC (AP) 0.897 (prevalence 0.407).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.788 vs 0.800; AP 0.660 vs 0.832; depth-4 fatal recall 0.705.

**Top summed importances:** REST_USE, EXTRICAT, NUMOCCS, PERMVIT, PCRASH5 (associations within FARS fatal crashes, not causal effects).
