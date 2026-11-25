**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.626) on holdout:** accuracy 0.745, balanced accuracy 0.649, precision 0.653, recall 0.393, fatal F1 0.491, macro-F1 0.661, ROC-AUC 0.782, PR-AUC (AP) 0.615 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.647, ROC-AUC 0.777, AP 0.603.

**Tuned decision tree, same holdout:** ROC-AUC 0.758, PR-AUC (AP) 0.584, balanced accuracy 0.648, macro-F1 0.658.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
