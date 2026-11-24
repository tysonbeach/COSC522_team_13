**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.789) on holdout:** accuracy 0.825, balanced accuracy 0.785, precision 0.740, recall 0.679, fatal F1 0.708, macro-F1 0.792, ROC-AUC 0.893, PR-AUC (AP) 0.789 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.779, ROC-AUC 0.888, AP 0.776.

**Tuned decision tree, same holdout:** ROC-AUC 0.854, PR-AUC (AP) 0.717, balanced accuracy 0.748, macro-F1 0.755.

**Top summed importances:** P_CRASH2, EXTRICAT, HARM_EV, BODY_TYP, EJECTION (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
