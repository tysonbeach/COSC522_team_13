**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.795) on holdout:** accuracy 0.771, balanced accuracy 0.749, precision 0.779, recall 0.622, fatal F1 0.692, macro-F1 0.755, ROC-AUC 0.842, PR-AUC (AP) 0.799 (prevalence 0.413).

**Default settings on holdout:** balanced accuracy 0.747, ROC-AUC 0.837, AP 0.788.

**Tuned decision tree, same holdout:** ROC-AUC 0.822, PR-AUC (AP) 0.779, balanced accuracy 0.739, macro-F1 0.744.

**Top summed importances:** REST_USE, BODY_TYP, AGE, MOD_YEAR, PER_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
