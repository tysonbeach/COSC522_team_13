**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.735) on holdout:** accuracy 0.800, balanced accuracy 0.749, precision 0.706, recall 0.613, fatal F1 0.656, macro-F1 0.758, ROC-AUC 0.864, PR-AUC (AP) 0.741 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.747, ROC-AUC 0.860, AP 0.732.

**Tuned decision tree, same holdout:** ROC-AUC 0.813, PR-AUC (AP) 0.654, balanced accuracy 0.697, macro-F1 0.707.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, IMPACT1, REST_USE (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
