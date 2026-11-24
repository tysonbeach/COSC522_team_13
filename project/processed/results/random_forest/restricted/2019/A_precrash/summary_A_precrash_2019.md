**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.623) on holdout:** accuracy 0.756, balanced accuracy 0.664, precision 0.681, recall 0.417, fatal F1 0.517, macro-F1 0.677, ROC-AUC 0.781, PR-AUC (AP) 0.635 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.654, ROC-AUC 0.777, AP 0.616.

**Tuned decision tree, same holdout:** ROC-AUC 0.756, PR-AUC (AP) 0.600, balanced accuracy 0.654, macro-F1 0.665.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
