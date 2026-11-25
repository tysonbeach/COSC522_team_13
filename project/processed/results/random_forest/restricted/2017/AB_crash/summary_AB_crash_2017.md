**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.703) on holdout:** accuracy 0.780, balanced accuracy 0.707, precision 0.700, recall 0.514, fatal F1 0.593, macro-F1 0.721, ROC-AUC 0.842, PR-AUC (AP) 0.703 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.689, ROC-AUC 0.835, AP 0.685.

**Tuned decision tree, same holdout:** ROC-AUC 0.796, PR-AUC (AP) 0.637, balanced accuracy 0.673, macro-F1 0.683.

**Top summed importances:** AGE, REST_USE, HOUR, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
