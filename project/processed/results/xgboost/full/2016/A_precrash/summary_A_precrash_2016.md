**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.795) on holdout:** accuracy 0.777, balanced accuracy 0.758, precision 0.752, recall 0.662, fatal F1 0.704, macro-F1 0.762, ROC-AUC 0.848, PR-AUC (AP) 0.792 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.756, ROC-AUC 0.844, AP 0.787.

**Tuned decision tree, same holdout:** ROC-AUC 0.817, PR-AUC (AP) 0.760, balanced accuracy 0.734, macro-F1 0.739.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
