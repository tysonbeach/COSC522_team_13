**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.882) on holdout:** accuracy 0.824, balanced accuracy 0.808, precision 0.816, recall 0.726, fatal F1 0.768, macro-F1 0.813, ROC-AUC 0.907, PR-AUC (AP) 0.882 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.798, ROC-AUC 0.899, AP 0.869.

**Tuned decision tree, same holdout:** ROC-AUC 0.881, PR-AUC (AP) 0.853, balanced accuracy 0.785, macro-F1 0.789.

**Top summed importances:** REST_USE, AGE, PERMVIT, BODY_TYP, PCRASH5 (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
