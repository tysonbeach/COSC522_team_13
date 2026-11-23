**Feature block:** A_precrash (25 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.749, balanced accuracy 0.662, precision 0.645, recall 0.433, fatal F1 0.518, macro-F1 0.674, ROC-AUC 0.766, PR-AUC (AP) 0.600 (prevalence 0.312).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.623 vs 0.652; AP 0.393 vs 0.549; depth-4 fatal recall 0.409.

**Top summed importances:** REST_USE, AGE, BODY_TYP, PER_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
