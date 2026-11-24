**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 53,046 occupants from 16,586 crashes; holdout 10,522 occupants / 3,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.729) on holdout:** accuracy 0.792, balanced accuracy 0.735, precision 0.705, recall 0.582, fatal F1 0.637, macro-F1 0.746, ROC-AUC 0.860, PR-AUC (AP) 0.730 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.736, ROC-AUC 0.857, AP 0.722.

**Tuned decision tree, same holdout:** ROC-AUC 0.806, PR-AUC (AP) 0.650, balanced accuracy 0.695, macro-F1 0.706.

**Top summed importances:** P_CRASH2, BODY_TYP, HARM_EV, IMPACT1, REST_USE (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
