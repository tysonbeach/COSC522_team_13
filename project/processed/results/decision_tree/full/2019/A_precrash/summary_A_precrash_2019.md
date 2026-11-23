**Feature block:** A_precrash (25 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.756, balanced accuracy 0.729, precision 0.732, recall 0.602, fatal F1 0.661, macro-F1 0.735, ROC-AUC 0.814, PR-AUC (AP) 0.754 (prevalence 0.394).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.665 vs 0.715; AP 0.512 vs 0.700; depth-4 fatal recall 0.552.

**Top summed importances:** REST_USE, AGE, SEAT_POS, BODY_TYP, MOD_YEAR (associations within FARS fatal crashes, not causal effects).
