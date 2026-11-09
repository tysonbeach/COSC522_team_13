**Feature set:** base_impact_post (46 features).

**Data:** 68,910 occupants from 31,371 crashes; holdout 13,856 occupants / 6,275 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.831, balanced accuracy 0.817, precision 0.814, recall 0.747, F1 0.779, ROC-AUC 0.916, PR-AUC (AP) 0.891 (prevalence 0.399).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.782 vs 0.790; AP 0.649 vs 0.823; depth-4 fatal recall 0.674.

**Top summed importances:** REST_USE, EXTRICAT, NUMOCCS, PERMVIT, PCRASH5 (associations within FARS fatal crashes, not causal effects).
