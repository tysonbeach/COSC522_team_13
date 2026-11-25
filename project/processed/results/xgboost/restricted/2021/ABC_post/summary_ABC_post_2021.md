**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.790) on holdout:** accuracy 0.826, balanced accuracy 0.786, precision 0.741, recall 0.680, fatal F1 0.709, macro-F1 0.792, ROC-AUC 0.898, PR-AUC (AP) 0.789 (prevalence 0.313).

**Default settings on holdout:** balanced accuracy 0.787, ROC-AUC 0.895, AP 0.780.

**Tuned decision tree, same holdout:** ROC-AUC 0.860, PR-AUC (AP) 0.723, balanced accuracy 0.751, macro-F1 0.758.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, EJECTION, EXTRICAT (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
