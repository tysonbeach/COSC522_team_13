**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.758) on holdout:** accuracy 0.818, balanced accuracy 0.772, precision 0.739, recall 0.648, fatal F1 0.691, macro-F1 0.781, ROC-AUC 0.889, PR-AUC (AP) 0.769 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.759, ROC-AUC 0.885, AP 0.759.

**Tuned decision tree, same holdout:** ROC-AUC 0.853, PR-AUC (AP) 0.710, balanced accuracy 0.743, macro-F1 0.750.

**Top summed importances:** EXTRICAT, AGE, EJECTION, REST_USE, PERMVIT (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
