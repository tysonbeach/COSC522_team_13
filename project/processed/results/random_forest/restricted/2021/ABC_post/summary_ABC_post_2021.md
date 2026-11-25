**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.769) on holdout:** accuracy 0.819, balanced accuracy 0.775, precision 0.736, recall 0.658, fatal F1 0.695, macro-F1 0.783, ROC-AUC 0.890, PR-AUC (AP) 0.773 (prevalence 0.313).

**Default settings on holdout:** balanced accuracy 0.766, ROC-AUC 0.885, AP 0.759.

**Tuned decision tree, same holdout:** ROC-AUC 0.860, PR-AUC (AP) 0.723, balanced accuracy 0.751, macro-F1 0.758.

**Top summed importances:** EXTRICAT, EJECTION, AGE, REST_USE, PERMVIT (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
