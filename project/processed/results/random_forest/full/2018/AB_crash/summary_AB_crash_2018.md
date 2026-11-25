**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.881) on holdout:** accuracy 0.828, balanced accuracy 0.812, precision 0.820, recall 0.732, fatal F1 0.773, macro-F1 0.817, ROC-AUC 0.910, PR-AUC (AP) 0.884 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.803, ROC-AUC 0.902, AP 0.872.

**Tuned decision tree, same holdout:** ROC-AUC 0.880, PR-AUC (AP) 0.850, balanced accuracy 0.779, macro-F1 0.784.

**Top summed importances:** REST_USE, PERMVIT, AGE, BODY_TYP, P_CRASH2 (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
