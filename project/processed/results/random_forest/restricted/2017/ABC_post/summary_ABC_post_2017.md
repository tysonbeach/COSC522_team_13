**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.760) on holdout:** accuracy 0.818, balanced accuracy 0.769, precision 0.740, recall 0.639, fatal F1 0.686, macro-F1 0.779, ROC-AUC 0.884, PR-AUC (AP) 0.762 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.760, ROC-AUC 0.881, AP 0.747.

**Tuned decision tree, same holdout:** ROC-AUC 0.852, PR-AUC (AP) 0.713, balanced accuracy 0.745, macro-F1 0.750.

**Top summed importances:** EXTRICAT, AGE, EJECTION, REST_USE, PERMVIT (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
