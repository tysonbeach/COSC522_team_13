**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.624) on holdout:** accuracy 0.756, balanced accuracy 0.669, precision 0.666, recall 0.436, fatal F1 0.527, macro-F1 0.682, ROC-AUC 0.793, PR-AUC (AP) 0.637 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.662, ROC-AUC 0.786, AP 0.621.

**Tuned decision tree, same holdout:** ROC-AUC 0.766, PR-AUC (AP) 0.595, balanced accuracy 0.659, macro-F1 0.669.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
