**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.783) on holdout:** accuracy 0.770, balanced accuracy 0.741, precision 0.770, recall 0.601, fatal F1 0.675, macro-F1 0.749, ROC-AUC 0.835, PR-AUC (AP) 0.783 (prevalence 0.398).

**Default settings on holdout:** balanced accuracy 0.736, ROC-AUC 0.827, AP 0.772.

**Tuned decision tree, same holdout:** ROC-AUC 0.817, PR-AUC (AP) 0.766, balanced accuracy 0.732, macro-F1 0.738.

**Top summed importances:** REST_USE, AGE, BODY_TYP, SEAT_POS, MOD_YEAR (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
