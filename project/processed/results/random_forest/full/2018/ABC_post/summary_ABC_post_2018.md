**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.907) on holdout:** accuracy 0.845, balanced accuracy 0.836, precision 0.821, recall 0.787, fatal F1 0.804, macro-F1 0.838, ROC-AUC 0.930, PR-AUC (AP) 0.906 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.830, ROC-AUC 0.926, AP 0.898.

**Tuned decision tree, same holdout:** ROC-AUC 0.911, PR-AUC (AP) 0.883, balanced accuracy 0.818, macro-F1 0.820.

**Top summed importances:** EJECTION, REST_USE, EXTRICAT, PERMVIT, AGE (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
