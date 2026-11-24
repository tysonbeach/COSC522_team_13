**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.726) on holdout:** accuracy 0.790, balanced accuracy 0.732, precision 0.694, recall 0.578, fatal F1 0.631, macro-F1 0.742, ROC-AUC 0.853, PR-AUC (AP) 0.728 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.724, ROC-AUC 0.847, AP 0.720.

**Tuned decision tree, same holdout:** ROC-AUC 0.796, PR-AUC (AP) 0.637, balanced accuracy 0.673, macro-F1 0.683.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, REST_USE, IMPACT1 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
