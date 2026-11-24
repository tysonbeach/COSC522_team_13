**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.1, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.896) on holdout:** accuracy 0.835, balanced accuracy 0.823, precision 0.826, recall 0.760, fatal F1 0.791, macro-F1 0.827, ROC-AUC 0.919, PR-AUC (AP) 0.900 (prevalence 0.413).

**Default settings on holdout:** balanced accuracy 0.819, ROC-AUC 0.916, AP 0.897.

**Tuned decision tree, same holdout:** ROC-AUC 0.883, PR-AUC (AP) 0.863, balanced accuracy 0.784, macro-F1 0.787.

**Top summed importances:** P_CRASH2, HARM_EV, REST_USE, BODY_TYP, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
