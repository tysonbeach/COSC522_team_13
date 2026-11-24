**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.614) on holdout:** accuracy 0.748, balanced accuracy 0.652, precision 0.656, recall 0.399, fatal F1 0.496, macro-F1 0.664, ROC-AUC 0.783, PR-AUC (AP) 0.619 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.642, ROC-AUC 0.771, AP 0.597.

**Tuned decision tree, same holdout:** ROC-AUC 0.759, PR-AUC (AP) 0.591, balanced accuracy 0.652, macro-F1 0.663.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
