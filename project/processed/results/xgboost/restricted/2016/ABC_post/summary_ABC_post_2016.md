**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.782) on holdout:** accuracy 0.826, balanced accuracy 0.787, precision 0.742, recall 0.684, fatal F1 0.712, macro-F1 0.794, ROC-AUC 0.895, PR-AUC (AP) 0.787 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.779, ROC-AUC 0.891, AP 0.778.

**Tuned decision tree, same holdout:** ROC-AUC 0.853, PR-AUC (AP) 0.710, balanced accuracy 0.743, macro-F1 0.750.

**Top summed importances:** P_CRASH2, BODY_TYP, HARM_EV, DEFORMED, EJECTION (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
