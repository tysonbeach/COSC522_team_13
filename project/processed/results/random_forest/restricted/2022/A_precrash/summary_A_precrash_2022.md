**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.635) on holdout:** accuracy 0.756, balanced accuracy 0.670, precision 0.664, recall 0.442, fatal F1 0.531, macro-F1 0.683, ROC-AUC 0.791, PR-AUC (AP) 0.637 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.663, ROC-AUC 0.782, AP 0.616.

**Tuned decision tree, same holdout:** ROC-AUC 0.766, PR-AUC (AP) 0.600, balanced accuracy 0.662, macro-F1 0.674.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
