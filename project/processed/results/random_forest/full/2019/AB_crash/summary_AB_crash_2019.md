**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.880) on holdout:** accuracy 0.824, balanced accuracy 0.805, precision 0.816, recall 0.714, fatal F1 0.762, macro-F1 0.811, ROC-AUC 0.908, PR-AUC (AP) 0.879 (prevalence 0.394).

**Default settings on holdout:** balanced accuracy 0.795, ROC-AUC 0.902, AP 0.869.

**Tuned decision tree, same holdout:** ROC-AUC 0.882, PR-AUC (AP) 0.851, balanced accuracy 0.779, macro-F1 0.784.

**Top summed importances:** REST_USE, AGE, PERMVIT, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
