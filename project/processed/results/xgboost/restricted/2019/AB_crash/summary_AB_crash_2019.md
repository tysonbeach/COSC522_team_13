**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.732) on holdout:** accuracy 0.791, balanced accuracy 0.736, precision 0.699, recall 0.587, fatal F1 0.638, macro-F1 0.746, ROC-AUC 0.857, PR-AUC (AP) 0.742 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.735, ROC-AUC 0.853, AP 0.735.

**Tuned decision tree, same holdout:** ROC-AUC 0.808, PR-AUC (AP) 0.651, balanced accuracy 0.695, macro-F1 0.703.

**Top summed importances:** P_CRASH2, BODY_TYP, HARM_EV, REST_USE, IMPACT1 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
