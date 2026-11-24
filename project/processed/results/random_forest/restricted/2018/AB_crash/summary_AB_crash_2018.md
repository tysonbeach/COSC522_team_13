**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.714) on holdout:** accuracy 0.792, balanced accuracy 0.727, precision 0.713, recall 0.555, fatal F1 0.624, macro-F1 0.740, ROC-AUC 0.852, PR-AUC (AP) 0.717 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.714, ROC-AUC 0.846, AP 0.707.

**Tuned decision tree, same holdout:** ROC-AUC 0.813, PR-AUC (AP) 0.654, balanced accuracy 0.697, macro-F1 0.707.

**Top summed importances:** AGE, REST_USE, HOUR, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
