**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.905) on holdout:** accuracy 0.847, balanced accuracy 0.837, precision 0.817, recall 0.788, fatal F1 0.802, macro-F1 0.839, ROC-AUC 0.930, PR-AUC (AP) 0.902 (prevalence 0.394).

**Default settings on holdout:** balanced accuracy 0.831, ROC-AUC 0.926, AP 0.894.

**Tuned decision tree, same holdout:** ROC-AUC 0.911, PR-AUC (AP) 0.881, balanced accuracy 0.817, macro-F1 0.819.

**Top summed importances:** REST_USE, EJECTION, EXTRICAT, PERMVIT, AGE (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
