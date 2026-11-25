**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.787) on holdout:** accuracy 0.822, balanced accuracy 0.782, precision 0.732, recall 0.677, fatal F1 0.703, macro-F1 0.788, ROC-AUC 0.896, PR-AUC (AP) 0.792 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.780, ROC-AUC 0.894, AP 0.786.

**Tuned decision tree, same holdout:** ROC-AUC 0.855, PR-AUC (AP) 0.719, balanced accuracy 0.743, macro-F1 0.751.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, EXTRICAT, EJECTION (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
