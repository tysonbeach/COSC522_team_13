**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.891) on holdout:** accuracy 0.834, balanced accuracy 0.821, precision 0.816, recall 0.757, fatal F1 0.785, macro-F1 0.825, ROC-AUC 0.917, PR-AUC (AP) 0.893 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.817, ROC-AUC 0.913, AP 0.889.

**Tuned decision tree, same holdout:** ROC-AUC 0.880, PR-AUC (AP) 0.850, balanced accuracy 0.779, macro-F1 0.784.

**Top summed importances:** HARM_EV, P_CRASH2, REST_USE, BODY_TYP, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
