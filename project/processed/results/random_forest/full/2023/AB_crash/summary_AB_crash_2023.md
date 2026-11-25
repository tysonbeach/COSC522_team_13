**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.883) on holdout:** accuracy 0.827, balanced accuracy 0.809, precision 0.827, recall 0.717, fatal F1 0.768, macro-F1 0.815, ROC-AUC 0.911, PR-AUC (AP) 0.886 (prevalence 0.400).

**Default settings on holdout:** balanced accuracy 0.799, ROC-AUC 0.905, AP 0.876.

**Tuned decision tree, same holdout:** ROC-AUC 0.889, PR-AUC (AP) 0.860, balanced accuracy 0.785, macro-F1 0.791.

**Top summed importances:** REST_USE, BODY_TYP, AGE, P_CRASH2, PERMVIT (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
