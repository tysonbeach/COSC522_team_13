**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.1, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.895) on holdout:** accuracy 0.833, balanced accuracy 0.821, precision 0.817, recall 0.757, fatal F1 0.786, macro-F1 0.824, ROC-AUC 0.917, PR-AUC (AP) 0.896 (prevalence 0.406).

**Default settings on holdout:** balanced accuracy 0.814, ROC-AUC 0.914, AP 0.892.

**Tuned decision tree, same holdout:** ROC-AUC 0.881, PR-AUC (AP) 0.857, balanced accuracy 0.782, macro-F1 0.788.

**Top summed importances:** HARM_EV, P_CRASH2, BODY_TYP, REST_USE, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
