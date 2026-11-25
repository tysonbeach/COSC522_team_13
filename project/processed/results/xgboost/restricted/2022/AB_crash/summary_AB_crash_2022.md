**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.734) on holdout:** accuracy 0.795, balanced accuracy 0.741, precision 0.703, recall 0.597, fatal F1 0.645, macro-F1 0.751, ROC-AUC 0.860, PR-AUC (AP) 0.733 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.738, ROC-AUC 0.856, AP 0.721.

**Tuned decision tree, same holdout:** ROC-AUC 0.806, PR-AUC (AP) 0.642, balanced accuracy 0.690, macro-F1 0.701.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, REST_USE, IMPACT1 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
