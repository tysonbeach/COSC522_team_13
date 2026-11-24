**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.765) on holdout:** accuracy 0.816, balanced accuracy 0.769, precision 0.735, recall 0.643, fatal F1 0.686, macro-F1 0.778, ROC-AUC 0.886, PR-AUC (AP) 0.770 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.762, ROC-AUC 0.884, AP 0.758.

**Tuned decision tree, same holdout:** ROC-AUC 0.855, PR-AUC (AP) 0.719, balanced accuracy 0.743, macro-F1 0.751.

**Top summed importances:** EXTRICAT, AGE, EJECTION, REST_USE, AIR_BAG (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
