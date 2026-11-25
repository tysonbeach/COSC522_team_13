**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 51,300 occupants from 16,222 crashes; holdout 10,152 occupants / 3,245 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.794) on holdout:** accuracy 0.824, balanced accuracy 0.783, precision 0.738, recall 0.675, fatal F1 0.705, macro-F1 0.790, ROC-AUC 0.896, PR-AUC (AP) 0.788 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.783, ROC-AUC 0.893, AP 0.781.

**Tuned decision tree, same holdout:** ROC-AUC 0.856, PR-AUC (AP) 0.718, balanced accuracy 0.743, macro-F1 0.752.

**Top summed importances:** P_CRASH2, DEFORMED, BODY_TYP, HARM_EV, EXTRICAT (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
