**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 3, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.626) on holdout:** accuracy 0.752, balanced accuracy 0.663, precision 0.657, recall 0.426, fatal F1 0.517, macro-F1 0.675, ROC-AUC 0.790, PR-AUC (AP) 0.633 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.671, ROC-AUC 0.785, AP 0.625.

**Tuned decision tree, same holdout:** ROC-AUC 0.759, PR-AUC (AP) 0.591, balanced accuracy 0.652, macro-F1 0.663.

**Top summed importances:** BODY_TYP, REST_USE, SEAT_POS, HOUR, TOW_VEH (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
