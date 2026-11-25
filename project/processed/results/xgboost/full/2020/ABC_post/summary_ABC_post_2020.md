**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.921) on holdout:** accuracy 0.858, balanced accuracy 0.852, precision 0.840, recall 0.812, fatal F1 0.826, macro-F1 0.853, ROC-AUC 0.941, PR-AUC (AP) 0.923 (prevalence 0.413).

**Default settings on holdout:** balanced accuracy 0.849, ROC-AUC 0.938, AP 0.920.

**Tuned decision tree, same holdout:** ROC-AUC 0.917, PR-AUC (AP) 0.895, balanced accuracy 0.826, macro-F1 0.828.

**Top summed importances:** REST_USE, HARM_EV, P_CRASH2, PCRASH5, EXTRICAT (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
