**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.908) on holdout:** accuracy 0.851, balanced accuracy 0.839, precision 0.835, recall 0.782, fatal F1 0.807, macro-F1 0.843, ROC-AUC 0.932, PR-AUC (AP) 0.907 (prevalence 0.400).

**Default settings on holdout:** balanced accuracy 0.832, ROC-AUC 0.928, AP 0.900.

**Tuned decision tree, same holdout:** ROC-AUC 0.917, PR-AUC (AP) 0.890, balanced accuracy 0.823, macro-F1 0.826.

**Top summed importances:** EJECTION, REST_USE, EXTRICAT, PERMVIT, AGE (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
