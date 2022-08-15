from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
import numpy as np
import sys

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import RandomizedSearchCV

from src.global_config import *


class RandomForest:

    # Define parameters to evaluate
    # the number of trees to build before taking the maximum voting or averages of predictions
    n_estimators_values = [int(x) for x in np.linspace(10, 500, num=100)]  # np.arange(100, 810, 10).tolist()
    criterion_values = ['gini']
    class_weight_values = ['balanced']
    max_features_values = ['auto', 'sqrt']
    max_depth_values = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth_values.append(None)
    min_samples_split_values = [2, 5, 10]
    min_samples_leaf_values = [1, 2, 4]
    bootstrap_values = [True, False]

    parameters = {'n_estimators': n_estimators_values,
                  'criterion': criterion_values,
                  'max_features': max_features_values,
                  'max_depth': max_depth_values,
                  'min_samples_split': min_samples_split_values,
                  'min_samples_leaf': min_samples_leaf_values,
                  'bootstrap': bootstrap_values,
                  'random_state': [seed],
                  'class_weight': class_weight_values,
                  }

    @classmethod
    def param_search(cls, data, test=False):
        if test:
            cls.parameters = {}

        rf = RandomForestClassifier()
        logo = LeaveOneGroupOut()

        # Reduce the number of possible combinations by randomly resampling to 5000 combinations
        clf = RandomizedSearchCV(estimator=rf,
                                 param_distributions=cls.parameters,
                                 scoring='roc_auc_ovo_weighted',
                                 cv=logo.split(X=data.X_list, groups=data.groups),
                                 verbose=51,
                                 n_iter=5000,
                                 random_state=seed,
                                 n_jobs=-25,
                                 pre_dispatch='n_jobs'
                                 )
        clf.fit(data.X_list, data.y_list)

        return clf
