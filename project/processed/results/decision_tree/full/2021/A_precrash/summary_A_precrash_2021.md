**Feature block:** A_precrash (25 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.760, balanced accuracy 0.737, precision 0.748, recall 0.616, fatal F1 0.676, macro-F1 0.743, ROC-AUC 0.823, PR-AUC (AP) 0.770 (prevalence 0.406).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.670 vs 0.714; AP 0.528 vs 0.716; depth-4 fatal recall 0.536.

**Top summed importances:** REST_USE, PER_TYP, AGE, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
