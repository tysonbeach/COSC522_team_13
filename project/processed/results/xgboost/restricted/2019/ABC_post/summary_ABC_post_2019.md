**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.785) on holdout:** accuracy 0.822, balanced accuracy 0.782, precision 0.736, recall 0.674, fatal F1 0.703, macro-F1 0.788, ROC-AUC 0.892, PR-AUC (AP) 0.797 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.780, ROC-AUC 0.888, AP 0.787.

**Tuned decision tree, same holdout:** ROC-AUC 0.848, PR-AUC (AP) 0.723, balanced accuracy 0.745, macro-F1 0.753.

**Top summed importances:** P_CRASH2, HARM_EV, EXTRICAT, BODY_TYP, DEFORMED (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
