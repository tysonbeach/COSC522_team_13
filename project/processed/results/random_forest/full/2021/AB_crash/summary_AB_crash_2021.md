**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.884) on holdout:** accuracy 0.822, balanced accuracy 0.806, precision 0.820, recall 0.719, fatal F1 0.767, macro-F1 0.812, ROC-AUC 0.908, PR-AUC (AP) 0.885 (prevalence 0.406).

**Default settings on holdout:** balanced accuracy 0.801, ROC-AUC 0.904, AP 0.878.

**Tuned decision tree, same holdout:** ROC-AUC 0.881, PR-AUC (AP) 0.857, balanced accuracy 0.782, macro-F1 0.788.

**Top summed importances:** REST_USE, PERMVIT, BODY_TYP, AGE, P_CRASH2 (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
