**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.792) on holdout:** accuracy 0.768, balanced accuracy 0.744, precision 0.768, recall 0.615, fatal F1 0.683, macro-F1 0.750, ROC-AUC 0.841, PR-AUC (AP) 0.791 (prevalence 0.406).

**Default settings on holdout:** balanced accuracy 0.740, ROC-AUC 0.835, AP 0.784.

**Tuned decision tree, same holdout:** ROC-AUC 0.823, PR-AUC (AP) 0.770, balanced accuracy 0.737, macro-F1 0.743.

**Top summed importances:** REST_USE, BODY_TYP, AGE, MOD_YEAR, PER_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
