**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.708) on holdout:** accuracy 0.779, balanced accuracy 0.708, precision 0.702, recall 0.518, fatal F1 0.596, macro-F1 0.722, ROC-AUC 0.840, PR-AUC (AP) 0.702 (prevalence 0.315).

**Default settings on holdout:** balanced accuracy 0.699, ROC-AUC 0.837, AP 0.688.

**Tuned decision tree, same holdout:** ROC-AUC 0.793, PR-AUC (AP) 0.631, balanced accuracy 0.681, macro-F1 0.691.

**Top summed importances:** REST_USE, AGE, PERMVIT, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
