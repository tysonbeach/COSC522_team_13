**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.711) on holdout:** accuracy 0.787, balanced accuracy 0.716, precision 0.715, recall 0.529, fatal F1 0.608, macro-F1 0.731, ROC-AUC 0.848, PR-AUC (AP) 0.714 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.706, ROC-AUC 0.844, AP 0.700.

**Tuned decision tree, same holdout:** ROC-AUC 0.806, PR-AUC (AP) 0.642, balanced accuracy 0.690, macro-F1 0.701.

**Top summed importances:** AGE, REST_USE, PERMVIT, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
