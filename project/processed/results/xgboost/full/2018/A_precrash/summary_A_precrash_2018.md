**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.790) on holdout:** accuracy 0.777, balanced accuracy 0.758, precision 0.755, recall 0.659, fatal F1 0.704, macro-F1 0.763, ROC-AUC 0.846, PR-AUC (AP) 0.795 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.755, ROC-AUC 0.841, AP 0.787.

**Tuned decision tree, same holdout:** ROC-AUC 0.815, PR-AUC (AP) 0.761, balanced accuracy 0.733, macro-F1 0.738.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
