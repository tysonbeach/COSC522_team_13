**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.914) on holdout:** accuracy 0.858, balanced accuracy 0.851, precision 0.831, recall 0.813, fatal F1 0.822, macro-F1 0.852, ROC-AUC 0.936, PR-AUC (AP) 0.914 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.847, ROC-AUC 0.934, AP 0.912.

**Tuned decision tree, same holdout:** ROC-AUC 0.910, PR-AUC (AP) 0.882, balanced accuracy 0.819, macro-F1 0.820.

**Top summed importances:** HARM_EV, P_CRASH2, PCRASH5, EJECTION, EXTRICAT (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
