**Feature set:** base (26 features).

**Data:** 71,957 occupants from 32,435 crashes; holdout 14,578 occupants / 6,487 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.761, balanced accuracy 0.734, precision 0.752, recall 0.600, F1 0.668, ROC-AUC 0.826, PR-AUC (AP) 0.783 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.689 vs 0.716; AP 0.541 vs 0.731; depth-4 fatal recall 0.543.

**Top summed importances:** REST_USE, NUMOCCS, AGE, VSPD_LIM, VALIGN (associations within FARS fatal crashes, not causal effects).
