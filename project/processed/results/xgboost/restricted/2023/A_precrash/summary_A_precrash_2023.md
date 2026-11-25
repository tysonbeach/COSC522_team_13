**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 200, 'model__subsample': 0.8}; mean CV AP 0.636) on holdout:** accuracy 0.752, balanced accuracy 0.670, precision 0.649, recall 0.452, fatal F1 0.533, macro-F1 0.682, ROC-AUC 0.791, PR-AUC (AP) 0.628 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.676, ROC-AUC 0.785, AP 0.619.

**Tuned decision tree, same holdout:** ROC-AUC 0.758, PR-AUC (AP) 0.584, balanced accuracy 0.648, macro-F1 0.658.

**Top summed importances:** BODY_TYP, REST_USE, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
