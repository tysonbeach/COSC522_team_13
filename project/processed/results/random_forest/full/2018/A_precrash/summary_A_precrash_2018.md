**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.780) on holdout:** accuracy 0.770, balanced accuracy 0.744, precision 0.769, recall 0.610, fatal F1 0.681, macro-F1 0.750, ROC-AUC 0.838, PR-AUC (AP) 0.785 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.738, ROC-AUC 0.834, AP 0.776.

**Tuned decision tree, same holdout:** ROC-AUC 0.815, PR-AUC (AP) 0.761, balanced accuracy 0.733, macro-F1 0.738.

**Top summed importances:** REST_USE, BODY_TYP, AGE, MOD_YEAR, PER_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
