**Feature block:** AB_crash (38 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.799, balanced accuracy 0.779, precision 0.781, recall 0.682, fatal F1 0.728, macro-F1 0.784, ROC-AUC 0.882, PR-AUC (AP) 0.851 (prevalence 0.394).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.746 vs 0.754; AP 0.600 vs 0.778; depth-4 fatal recall 0.621.

**Top summed importances:** REST_USE, PERMVIT, PCRASH5, AGE, HARM_EV (associations within FARS fatal crashes, not causal effects).
