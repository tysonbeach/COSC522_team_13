**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.794) on holdout:** accuracy 0.778, balanced accuracy 0.756, precision 0.758, recall 0.648, fatal F1 0.699, macro-F1 0.761, ROC-AUC 0.847, PR-AUC (AP) 0.795 (prevalence 0.398).

**Default settings on holdout:** balanced accuracy 0.751, ROC-AUC 0.841, AP 0.787.

**Tuned decision tree, same holdout:** ROC-AUC 0.817, PR-AUC (AP) 0.766, balanced accuracy 0.732, macro-F1 0.738.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
