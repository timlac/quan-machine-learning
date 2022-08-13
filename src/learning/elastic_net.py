import sys
import os
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDClassifier
from src.global_config import *
from src.learning.load_data import DataLoader
from src.learning.save_output import Saver
import time


class ElasticNet:
    # Define parameters to evaluate
    alpha_values = [0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.005, 0.0025, 0.0075, 0.01, 0.05, 0.1, 1]
    n_iter_no_change_values = [20, 50, 100, 150]
    l1_ratio_values = [0.049, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
                       0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.89, 0.95, 0.99]

    parameters = {'penalty': ['elasticnet'],
                  'class_weight': ['balanced'],
                  'loss': ['log'],
                  'random_state': [seed],
                  'alpha': alpha_values,
                  'l1_ratio': l1_ratio_values,
                  'n_iter_no_change': n_iter_no_change_values,
                  'max_iter': [2500]
                  }

    @classmethod
    def param_search(cls, data, test=False):
        if test:
            cls.parameters = {}

        elasticnet = SGDClassifier()
        logo = LeaveOneGroupOut()

        clf = GridSearchCV(estimator=elasticnet,
                           param_grid=cls.parameters,
                           scoring='roc_auc_ovo_weighted',
                           cv=logo.split(X=data.X, groups=data.groups),
                           verbose=51,
                           n_jobs=threads,
                           pre_dispatch='n_jobs'
                           )

        clf.fit(data.X, data.y)
        return clf
