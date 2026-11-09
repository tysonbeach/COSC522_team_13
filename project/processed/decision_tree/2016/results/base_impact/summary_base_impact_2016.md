**Feature set:** base_impact (40 features).

**Data:** 72,525 occupants from 32,698 crashes; holdout 14,661 occupants / 6,540 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.804, balanced accuracy 0.785, precision 0.790, recall 0.691, F1 0.737, ROC-AUC 0.888, PR-AUC (AP) 0.864 (prevalence 0.397).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.755 vs 0.770; AP 0.611 vs 0.809; depth-4 fatal recall 0.656.

**Top summed importances:** REST_USE, NUMOCCS, PERMVIT, PCRASH5, PERNOTMVIT (associations within FARS fatal crashes, not causal effects).
