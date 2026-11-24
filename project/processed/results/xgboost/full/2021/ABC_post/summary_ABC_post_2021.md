**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.920) on holdout:** accuracy 0.861, balanced accuracy 0.853, precision 0.843, recall 0.809, fatal F1 0.826, macro-F1 0.855, ROC-AUC 0.940, PR-AUC (AP) 0.921 (prevalence 0.406).

**Default settings on holdout:** balanced accuracy 0.848, ROC-AUC 0.938, AP 0.919.

**Tuned decision tree, same holdout:** ROC-AUC 0.915, PR-AUC (AP) 0.893, balanced accuracy 0.826, macro-F1 0.828.

**Top summed importances:** REST_USE, HARM_EV, P_CRASH2, PCRASH5, EXTRICAT (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
