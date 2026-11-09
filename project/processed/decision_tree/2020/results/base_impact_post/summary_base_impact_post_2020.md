**Feature set:** base_impact_post (46 features).

**Data:** 70,447 occupants from 33,199 crashes; holdout 14,138 occupants / 6,640 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.836, balanced accuracy 0.826, precision 0.824, recall 0.769, F1 0.795, ROC-AUC 0.920, PR-AUC (AP) 0.902 (prevalence 0.414).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.794 vs 0.807; AP 0.673 vs 0.842; depth-4 fatal recall 0.711.

**Top summed importances:** REST_USE, EXTRICAT, NUMOCCS, PCRASH5, PERMVIT (associations within FARS fatal crashes, not causal effects).
