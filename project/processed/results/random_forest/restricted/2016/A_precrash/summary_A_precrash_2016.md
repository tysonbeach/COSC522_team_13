**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.623) on holdout:** accuracy 0.756, balanced accuracy 0.663, precision 0.686, recall 0.412, fatal F1 0.515, macro-F1 0.676, ROC-AUC 0.794, PR-AUC (AP) 0.632 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.653, ROC-AUC 0.784, AP 0.612.

**Tuned decision tree, same holdout:** ROC-AUC 0.770, PR-AUC (AP) 0.597, balanced accuracy 0.662, macro-F1 0.673.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
