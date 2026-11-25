**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.634) on holdout:** accuracy 0.746, balanced accuracy 0.659, precision 0.649, recall 0.422, fatal F1 0.512, macro-F1 0.670, ROC-AUC 0.778, PR-AUC (AP) 0.615 (prevalence 0.315).

**Default settings on holdout:** balanced accuracy 0.654, ROC-AUC 0.771, AP 0.600.

**Tuned decision tree, same holdout:** ROC-AUC 0.757, PR-AUC (AP) 0.588, balanced accuracy 0.649, macro-F1 0.659.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
