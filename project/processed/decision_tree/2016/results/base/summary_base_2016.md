**Feature set:** base (26 features).

**Data:** 72,525 occupants from 32,698 crashes; holdout 14,661 occupants / 6,540 crashes, no crash overlap.

**Tuned tree ({'tree__ccp_alpha': 0.0, 'tree__max_depth': None, 'tree__min_samples_leaf': 100}) on holdout:** accuracy 0.772, balanced accuracy 0.746, precision 0.761, recall 0.620, F1 0.683, ROC-AUC 0.833, PR-AUC (AP) 0.793 (prevalence 0.397).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.692 vs 0.726; AP 0.542 vs 0.737; depth-4 fatal recall 0.581.

**Top summed importances:** REST_USE, NUMOCCS, AGE, RELJCT2, BODY_TYP (associations within FARS fatal crashes, not causal effects).
