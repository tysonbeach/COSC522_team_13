**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.770) on holdout:** accuracy 0.810, balanced accuracy 0.763, precision 0.725, recall 0.636, fatal F1 0.678, macro-F1 0.771, ROC-AUC 0.882, PR-AUC (AP) 0.761 (prevalence 0.315).

**Default settings on holdout:** balanced accuracy 0.760, ROC-AUC 0.880, AP 0.753.

**Tuned decision tree, same holdout:** ROC-AUC 0.853, PR-AUC (AP) 0.717, balanced accuracy 0.752, macro-F1 0.759.

**Top summed importances:** EXTRICAT, EJECTION, AGE, REST_USE, PERMVIT (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
