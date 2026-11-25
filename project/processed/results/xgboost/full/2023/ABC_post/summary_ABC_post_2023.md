**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.918) on holdout:** accuracy 0.858, balanced accuracy 0.849, precision 0.836, recall 0.802, fatal F1 0.819, macro-F1 0.851, ROC-AUC 0.939, PR-AUC (AP) 0.916 (prevalence 0.400).

**Default settings on holdout:** balanced accuracy 0.846, ROC-AUC 0.937, AP 0.915.

**Tuned decision tree, same holdout:** ROC-AUC 0.917, PR-AUC (AP) 0.890, balanced accuracy 0.823, macro-F1 0.826.

**Top summed importances:** REST_USE, HARM_EV, P_CRASH2, EXTRICAT, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
