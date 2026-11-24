**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.911) on holdout:** accuracy 0.852, balanced accuracy 0.844, precision 0.837, recall 0.798, fatal F1 0.817, macro-F1 0.847, ROC-AUC 0.934, PR-AUC (AP) 0.914 (prevalence 0.413).

**Default settings on holdout:** balanced accuracy 0.839, ROC-AUC 0.930, AP 0.907.

**Tuned decision tree, same holdout:** ROC-AUC 0.917, PR-AUC (AP) 0.895, balanced accuracy 0.826, macro-F1 0.828.

**Top summed importances:** REST_USE, EJECTION, EXTRICAT, PERMVIT, AGE (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
