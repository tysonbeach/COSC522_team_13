**Feature block:** ABC_post (44 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap.

**Tuned tree ({'model__ccp_alpha': 0.0, 'model__max_depth': None, 'model__min_samples_leaf': 100}) on holdout:** accuracy 0.834, balanced accuracy 0.823, precision 0.808, recall 0.768, fatal F1 0.788, macro-F1 0.826, ROC-AUC 0.917, PR-AUC (AP) 0.890 (prevalence 0.400).

**Baselines:** unrestricted vs depth 4 balanced accuracy 0.783 vs 0.799; AP 0.651 vs 0.816; depth-4 fatal recall 0.713.

**Top summed importances:** REST_USE, EXTRICAT, PERMVIT, PCRASH5, EJECTION (associations within FARS fatal crashes, not causal effects).
