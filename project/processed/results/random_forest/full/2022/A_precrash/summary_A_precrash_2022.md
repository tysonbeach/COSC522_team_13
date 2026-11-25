**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.801) on holdout:** accuracy 0.779, balanced accuracy 0.753, precision 0.775, recall 0.627, fatal F1 0.693, macro-F1 0.760, ROC-AUC 0.847, PR-AUC (AP) 0.797 (prevalence 0.399).

**Default settings on holdout:** balanced accuracy 0.747, ROC-AUC 0.841, AP 0.787.

**Tuned decision tree, same holdout:** ROC-AUC 0.830, PR-AUC (AP) 0.778, balanced accuracy 0.744, macro-F1 0.750.

**Top summed importances:** REST_USE, BODY_TYP, AGE, MOD_YEAR, PER_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
