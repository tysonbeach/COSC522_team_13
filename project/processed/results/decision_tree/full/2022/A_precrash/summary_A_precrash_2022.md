**Feature block:** A_precrash (25 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.767, balanced accuracy 0.744, precision 0.744, recall 0.633, fatal F1 0.684, macro-F1 0.750, ROC-AUC 0.830, PR-AUC (AP) 0.778 (prevalence 0.399).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.682 vs 0.725; AP 0.532 vs 0.722; depth-4 fatal recall 0.570.

**Top summed importances:** REST_USE, PER_TYP, AGE, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
