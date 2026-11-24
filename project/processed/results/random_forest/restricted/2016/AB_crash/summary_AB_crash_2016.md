**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.705) on holdout:** accuracy 0.791, balanced accuracy 0.723, precision 0.724, recall 0.541, fatal F1 0.619, macro-F1 0.738, ROC-AUC 0.850, PR-AUC (AP) 0.714 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.710, ROC-AUC 0.845, AP 0.707.

**Tuned decision tree, same holdout:** ROC-AUC 0.806, PR-AUC (AP) 0.650, balanced accuracy 0.695, macro-F1 0.706.

**Top summed importances:** AGE, REST_USE, HOUR, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
