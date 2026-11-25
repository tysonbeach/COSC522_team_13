**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 200, 'model__subsample': 0.8}; mean CV AP 0.634) on holdout:** accuracy 0.759, balanced accuracy 0.677, precision 0.671, recall 0.457, fatal F1 0.544, macro-F1 0.690, ROC-AUC 0.787, PR-AUC (AP) 0.641 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.679, ROC-AUC 0.785, AP 0.633.

**Tuned decision tree, same holdout:** ROC-AUC 0.756, PR-AUC (AP) 0.600, balanced accuracy 0.654, macro-F1 0.665.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, VTRAFCON (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
