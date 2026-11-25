**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.914) on holdout:** accuracy 0.851, balanced accuracy 0.838, precision 0.835, recall 0.779, fatal F1 0.806, macro-F1 0.842, ROC-AUC 0.934, PR-AUC (AP) 0.911 (prevalence 0.399).

**Default settings on holdout:** balanced accuracy 0.830, ROC-AUC 0.929, AP 0.901.

**Tuned decision tree, same holdout:** ROC-AUC 0.914, PR-AUC (AP) 0.888, balanced accuracy 0.818, macro-F1 0.821.

**Top summed importances:** REST_USE, EJECTION, EXTRICAT, PERMVIT, AGE (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
