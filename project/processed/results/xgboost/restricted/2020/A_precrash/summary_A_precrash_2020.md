**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.644) on holdout:** accuracy 0.750, balanced accuracy 0.681, precision 0.632, recall 0.496, fatal F1 0.556, macro-F1 0.691, ROC-AUC 0.786, PR-AUC (AP) 0.629 (prevalence 0.315).

**Default settings on holdout:** balanced accuracy 0.676, ROC-AUC 0.780, AP 0.617.

**Tuned decision tree, same holdout:** ROC-AUC 0.757, PR-AUC (AP) 0.588, balanced accuracy 0.649, macro-F1 0.659.

**Top summed importances:** BODY_TYP, REST_USE, SEAT_POS, HOUR, VTRAFCON (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
