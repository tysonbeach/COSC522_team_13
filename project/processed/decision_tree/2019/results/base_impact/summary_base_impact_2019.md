**Feature set:** base_impact (40 features).

**Data:** 68,910 occupants from 31,371 crashes; holdout 13,856 occupants / 6,275 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.804, balanced accuracy 0.784, precision 0.793, recall 0.687, F1 0.736, ROC-AUC 0.888, PR-AUC (AP) 0.864 (prevalence 0.399).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.753 vs 0.754; AP 0.612 vs 0.791; depth-4 fatal recall 0.619.

**Top summed importances:** REST_USE, PERMVIT, NUMOCCS, PCRASH5, PERNOTMVIT (associations within FARS fatal crashes, not causal effects).
