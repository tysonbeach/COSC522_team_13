**Feature set:** base_impact_post (46 features).

**Data:** 72,525 occupants from 32,698 crashes; holdout 14,661 occupants / 6,540 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.833, balanced accuracy 0.821, precision 0.807, recall 0.761, F1 0.783, ROC-AUC 0.913, PR-AUC (AP) 0.887 (prevalence 0.397).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.785 vs 0.792; AP 0.651 vs 0.812; depth-4 fatal recall 0.700.

**Top summed importances:** EJECTION, EXTRICAT, PERMVIT, PCRASH5, NUMOCCS (associations within FARS fatal crashes, not causal effects).
