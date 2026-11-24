**Model:** Random forest. **Feature block:** ABC_post (44 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.905) on holdout:** accuracy 0.849, balanced accuracy 0.839, precision 0.826, recall 0.787, fatal F1 0.806, macro-F1 0.841, ROC-AUC 0.929, PR-AUC (AP) 0.904 (prevalence 0.398).

**Default settings on holdout:** balanced accuracy 0.832, ROC-AUC 0.925, AP 0.896.

**Tuned decision tree, same holdout:** ROC-AUC 0.910, PR-AUC (AP) 0.880, balanced accuracy 0.814, macro-F1 0.817.

**Top summed importances:** EJECTION, REST_USE, EXTRICAT, PERMVIT, AGE (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
