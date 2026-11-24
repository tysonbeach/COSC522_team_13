**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.906) on holdout:** accuracy 0.851, balanced accuracy 0.843, precision 0.826, recall 0.799, fatal F1 0.812, macro-F1 0.844, ROC-AUC 0.930, PR-AUC (AP) 0.905 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.834, ROC-AUC 0.924, AP 0.894.

**Tuned decision tree, same holdout:** ROC-AUC 0.910, PR-AUC (AP) 0.882, balanced accuracy 0.819, macro-F1 0.820.

**Top summed importances:** EJECTION, REST_USE, PERMVIT, EXTRICAT, AGE (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
