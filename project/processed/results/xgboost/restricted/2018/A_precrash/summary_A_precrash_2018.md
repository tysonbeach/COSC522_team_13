**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 200, 'model__subsample': 0.8}; mean CV AP 0.636) on holdout:** accuracy 0.759, balanced accuracy 0.681, precision 0.657, recall 0.474, fatal F1 0.550, macro-F1 0.693, ROC-AUC 0.800, PR-AUC (AP) 0.648 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.683, ROC-AUC 0.792, AP 0.623.

**Tuned decision tree, same holdout:** ROC-AUC 0.766, PR-AUC (AP) 0.595, balanced accuracy 0.659, macro-F1 0.669.

**Top summed importances:** BODY_TYP, REST_USE, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
