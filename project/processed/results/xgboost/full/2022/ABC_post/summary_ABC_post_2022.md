**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.923) on holdout:** accuracy 0.858, balanced accuracy 0.847, precision 0.843, recall 0.791, fatal F1 0.816, macro-F1 0.850, ROC-AUC 0.939, PR-AUC (AP) 0.919 (prevalence 0.399).

**Default settings on holdout:** balanced accuracy 0.845, ROC-AUC 0.937, AP 0.915.

**Tuned decision tree, same holdout:** ROC-AUC 0.914, PR-AUC (AP) 0.888, balanced accuracy 0.818, macro-F1 0.821.

**Top summed importances:** REST_USE, HARM_EV, P_CRASH2, PCRASH5, EXTRICAT (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
