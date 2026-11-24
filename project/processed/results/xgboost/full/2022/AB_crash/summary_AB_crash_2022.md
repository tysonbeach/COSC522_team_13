**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.1, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.901) on holdout:** accuracy 0.833, balanced accuracy 0.821, precision 0.811, recall 0.759, fatal F1 0.784, macro-F1 0.824, ROC-AUC 0.919, PR-AUC (AP) 0.896 (prevalence 0.399).

**Default settings on holdout:** balanced accuracy 0.818, ROC-AUC 0.917, AP 0.893.

**Tuned decision tree, same holdout:** ROC-AUC 0.888, PR-AUC (AP) 0.859, balanced accuracy 0.789, macro-F1 0.793.

**Top summed importances:** HARM_EV, P_CRASH2, REST_USE, BODY_TYP, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
