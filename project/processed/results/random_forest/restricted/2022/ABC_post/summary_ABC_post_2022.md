**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.768) on holdout:** accuracy 0.817, balanced accuracy 0.771, precision 0.735, recall 0.647, fatal F1 0.688, macro-F1 0.779, ROC-AUC 0.884, PR-AUC (AP) 0.771 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.759, ROC-AUC 0.881, AP 0.761.

**Tuned decision tree, same holdout:** ROC-AUC 0.854, PR-AUC (AP) 0.717, balanced accuracy 0.748, macro-F1 0.755.

**Top summed importances:** EXTRICAT, AGE, EJECTION, REST_USE, AIR_BAG (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
