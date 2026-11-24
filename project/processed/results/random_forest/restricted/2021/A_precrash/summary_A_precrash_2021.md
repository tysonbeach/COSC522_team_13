**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.628) on holdout:** accuracy 0.751, balanced accuracy 0.662, precision 0.659, recall 0.424, fatal F1 0.516, macro-F1 0.674, ROC-AUC 0.791, PR-AUC (AP) 0.630 (prevalence 0.313).

**Default settings on holdout:** balanced accuracy 0.657, ROC-AUC 0.781, AP 0.613.

**Tuned decision tree, same holdout:** ROC-AUC 0.761, PR-AUC (AP) 0.592, balanced accuracy 0.650, macro-F1 0.660.

**Top summed importances:** REST_USE, AGE, BODY_TYP, MOD_YEAR, HOUR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
