**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.758) on holdout:** accuracy 0.815, balanced accuracy 0.767, precision 0.736, recall 0.639, fatal F1 0.684, macro-F1 0.776, ROC-AUC 0.881, PR-AUC (AP) 0.772 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.757, ROC-AUC 0.877, AP 0.757.

**Tuned decision tree, same holdout:** ROC-AUC 0.848, PR-AUC (AP) 0.723, balanced accuracy 0.745, macro-F1 0.753.

**Top summed importances:** EXTRICAT, AGE, REST_USE, EJECTION, PERMVIT (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
