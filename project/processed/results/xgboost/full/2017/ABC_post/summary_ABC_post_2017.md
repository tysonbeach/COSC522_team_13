**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.1, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.916) on holdout:** accuracy 0.857, balanced accuracy 0.848, precision 0.830, recall 0.804, fatal F1 0.817, macro-F1 0.850, ROC-AUC 0.936, PR-AUC (AP) 0.913 (prevalence 0.398).

**Default settings on holdout:** balanced accuracy 0.843, ROC-AUC 0.933, AP 0.910.

**Tuned decision tree, same holdout:** ROC-AUC 0.910, PR-AUC (AP) 0.880, balanced accuracy 0.814, macro-F1 0.817.

**Top summed importances:** HARM_EV, P_CRASH2, REST_USE, BODY_TYP, EXTRICAT (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
