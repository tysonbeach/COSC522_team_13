**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.795) on holdout:** accuracy 0.773, balanced accuracy 0.745, precision 0.778, recall 0.605, fatal F1 0.681, macro-F1 0.752, ROC-AUC 0.846, PR-AUC (AP) 0.798 (prevalence 0.400).

**Default settings on holdout:** balanced accuracy 0.744, ROC-AUC 0.840, AP 0.790.

**Tuned decision tree, same holdout:** ROC-AUC 0.824, PR-AUC (AP) 0.778, balanced accuracy 0.736, macro-F1 0.743.

**Top summed importances:** REST_USE, BODY_TYP, AGE, MOD_YEAR, PER_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
