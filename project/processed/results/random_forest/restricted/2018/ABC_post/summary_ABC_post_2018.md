**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.771) on holdout:** accuracy 0.814, balanced accuracy 0.764, precision 0.734, recall 0.631, fatal F1 0.679, macro-F1 0.774, ROC-AUC 0.885, PR-AUC (AP) 0.768 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.760, ROC-AUC 0.881, AP 0.752.

**Tuned decision tree, same holdout:** ROC-AUC 0.856, PR-AUC (AP) 0.718, balanced accuracy 0.743, macro-F1 0.752.

**Top summed importances:** EXTRICAT, AGE, EJECTION, REST_USE, PERMVIT (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
