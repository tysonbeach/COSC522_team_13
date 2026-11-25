**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 200, 'model__subsample': 0.8}; mean CV AP 0.637) on holdout:** accuracy 0.760, balanced accuracy 0.677, precision 0.675, recall 0.454, fatal F1 0.543, macro-F1 0.690, ROC-AUC 0.800, PR-AUC (AP) 0.637 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.679, ROC-AUC 0.796, AP 0.627.

**Tuned decision tree, same holdout:** ROC-AUC 0.770, PR-AUC (AP) 0.597, balanced accuracy 0.662, macro-F1 0.673.

**Top summed importances:** BODY_TYP, REST_USE, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
