**Feature set:** base (26 features).

**Data:** 79,885 occupants from 36,904 crashes; holdout 16,203 occupants / 7,381 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.772, balanced accuracy 0.750, precision 0.754, recall 0.639, F1 0.692, ROC-AUC 0.830, PR-AUC (AP) 0.792 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.684 vs 0.733; AP 0.536 vs 0.734; depth-4 fatal recall 0.632.

**Top summed importances:** REST_USE, NUMOCCS, AGE, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
