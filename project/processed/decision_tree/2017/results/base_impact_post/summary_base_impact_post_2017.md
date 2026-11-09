**Feature set:** base_impact_post (46 features).

**Data:** 71,957 occupants from 32,435 crashes; holdout 14,578 occupants / 6,487 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.829, balanced accuracy 0.815, precision 0.814, recall 0.743, F1 0.777, ROC-AUC 0.913, PR-AUC (AP) 0.886 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.784 vs 0.794; AP 0.653 vs 0.809; depth-4 fatal recall 0.700.

**Top summed importances:** EJECTION, EXTRICAT, PERMVIT, PCRASH5, NUMOCCS (associations within FARS fatal crashes, not causal effects).
