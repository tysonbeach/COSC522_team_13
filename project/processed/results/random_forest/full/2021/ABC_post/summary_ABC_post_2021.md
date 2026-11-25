**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.911) on holdout:** accuracy 0.852, balanced accuracy 0.843, precision 0.836, recall 0.791, fatal F1 0.813, macro-F1 0.845, ROC-AUC 0.933, PR-AUC (AP) 0.913 (prevalence 0.406).

**Default settings on holdout:** balanced accuracy 0.836, ROC-AUC 0.928, AP 0.903.

**Tuned decision tree, same holdout:** ROC-AUC 0.915, PR-AUC (AP) 0.893, balanced accuracy 0.826, macro-F1 0.828.

**Top summed importances:** REST_USE, EJECTION, EXTRICAT, PERMVIT, PCRASH5 (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
