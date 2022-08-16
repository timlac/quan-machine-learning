from sklearn.tree import DecisionTreeClassifier
import numpy as np

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import RandomizedSearchCV

from global_config import *


class DecisionTree:
    # Define parameters to evaluate
    criterion_values = ['gini', 'entropy']
    splitter_values = ['best', 'random']
    max_depth_values = np.arange(5, 55, 5).tolist()
    min_samples_split_values = np.linspace(0.1, 1.0, 10, endpoint=True)
    min_samples_leaf_values = np.linspace(0.1, 0.5, 5, endpoint=True)

    def __init__(self, data):
        self.data = data

        self.max_features_values = [int(x) for x in
                                    np.linspace(1, len(self.data.X_list.columns), num=18)]  # list(range(1,len(X.columns)))

        self.parameters = {'criterion': self.criterion_values,
                           'splitter': self.splitter_values,
                           'max_depth': self.max_depth_values,
                           'min_samples_split': self.min_samples_split_values,
                           'min_samples_leaf': self.min_samples_leaf_values,
                           'max_features': self.max_features_values,
                           'class_weight': ['balanced'],
                           'random_state': [seed]
                           }

    def param_search(self, test=False):
        if test:
            self.parameters = {}

        dt = DecisionTreeClassifier()
        logo = LeaveOneGroupOut()

        # Reduce the number of possible combinations by randomly resampling to 5000 combinations
        clf = RandomizedSearchCV(estimator=dt,
                                 param_distributions=self.parameters,
                                 scoring='roc_auc_ovo_weighted',
                                 cv=logo.split(X=self.data.X_list, groups=self.data.groups),
                                 verbose=51,
                                 random_state=seed,
                                 n_iter=5000,
                                 n_jobs=threads,
                                 pre_dispatch='n_jobs'
                                 )

        clf.fit(self.data.X_list, self.data.y_list)

        return clf
