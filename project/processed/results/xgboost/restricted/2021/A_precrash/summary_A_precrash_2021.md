**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 200, 'model__subsample': 0.8}; mean CV AP 0.638) on holdout:** accuracy 0.753, balanced accuracy 0.675, precision 0.647, recall 0.466, fatal F1 0.541, macro-F1 0.686, ROC-AUC 0.797, PR-AUC (AP) 0.636 (prevalence 0.313).

**Default settings on holdout:** balanced accuracy 0.678, ROC-AUC 0.792, AP 0.629.

**Tuned decision tree, same holdout:** ROC-AUC 0.761, PR-AUC (AP) 0.592, balanced accuracy 0.650, macro-F1 0.660.

**Top summed importances:** BODY_TYP, REST_USE, SEAT_POS, HOUR, VTRAFCON (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
