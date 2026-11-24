**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.890) on holdout:** accuracy 0.829, balanced accuracy 0.811, precision 0.824, recall 0.726, fatal F1 0.772, macro-F1 0.817, ROC-AUC 0.912, PR-AUC (AP) 0.886 (prevalence 0.399).

**Default settings on holdout:** balanced accuracy 0.801, ROC-AUC 0.905, AP 0.876.

**Tuned decision tree, same holdout:** ROC-AUC 0.888, PR-AUC (AP) 0.859, balanced accuracy 0.789, macro-F1 0.793.

**Top summed importances:** REST_USE, AGE, PERMVIT, BODY_TYP, P_CRASH2 (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
