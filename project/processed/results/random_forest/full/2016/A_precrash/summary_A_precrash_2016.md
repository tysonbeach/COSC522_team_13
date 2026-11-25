**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.785) on holdout:** accuracy 0.769, balanced accuracy 0.744, precision 0.765, recall 0.616, fatal F1 0.682, macro-F1 0.751, ROC-AUC 0.840, PR-AUC (AP) 0.784 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.742, ROC-AUC 0.834, AP 0.776.

**Tuned decision tree, same holdout:** ROC-AUC 0.817, PR-AUC (AP) 0.760, balanced accuracy 0.734, macro-F1 0.739.

**Top summed importances:** REST_USE, AGE, BODY_TYP, PER_TYP, MOD_YEAR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
