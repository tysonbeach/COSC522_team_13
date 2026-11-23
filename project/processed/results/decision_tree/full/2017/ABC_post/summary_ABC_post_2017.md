**Feature block:** ABC_post (44 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.826, balanced accuracy 0.814, precision 0.798, recall 0.753, fatal F1 0.775, macro-F1 0.817, ROC-AUC 0.910, PR-AUC (AP) 0.880 (prevalence 0.398).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.782 vs 0.799; AP 0.647 vs 0.808; depth-4 fatal recall 0.713.

**Top summed importances:** REST_USE, EXTRICAT, PERMVIT, PCRASH5, AGE (associations within FARS fatal crashes, not causal effects).
