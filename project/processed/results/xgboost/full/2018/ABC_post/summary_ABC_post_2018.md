**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 70,431 occupants from 32,028 crashes; holdout 14,077 occupants / 6,406 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.917) on holdout:** accuracy 0.855, balanced accuracy 0.846, precision 0.830, recall 0.802, fatal F1 0.816, macro-F1 0.848, ROC-AUC 0.937, PR-AUC (AP) 0.916 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.845, ROC-AUC 0.935, AP 0.914.

**Tuned decision tree, same holdout:** ROC-AUC 0.911, PR-AUC (AP) 0.883, balanced accuracy 0.818, macro-F1 0.820.

**Top summed importances:** HARM_EV, EXTRICAT, REST_USE, P_CRASH2, BODY_TYP (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
