**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.885) on holdout:** accuracy 0.825, balanced accuracy 0.811, precision 0.824, recall 0.731, fatal F1 0.775, macro-F1 0.816, ROC-AUC 0.911, PR-AUC (AP) 0.891 (prevalence 0.413).

**Default settings on holdout:** balanced accuracy 0.806, ROC-AUC 0.905, AP 0.882.

**Tuned decision tree, same holdout:** ROC-AUC 0.883, PR-AUC (AP) 0.863, balanced accuracy 0.784, macro-F1 0.787.

**Top summed importances:** REST_USE, PERMVIT, AGE, BODY_TYP, P_CRASH2 (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
