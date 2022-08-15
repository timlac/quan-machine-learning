from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_validate
import numpy as np
import sys

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import GridSearchCV

from src.global_config import *


class KNN:
    # Define other to evaluate
    leaf_size_values = [10, 20, 30]
    algorithm_values = ['ball_tree', 'brute', 'kd_tree']

    def __init__(self, data):
        self.data = data

        # we want to evaluate different number of neighbors (clusters) based on the size of the training set.
        # set a cluster floor at the number of targets
        floor = len(data.y_list.unique())
        # set a cluster cap equal to 3/4:ths of the size of the training set.
        # size of training set is equal to all datapoints minus the size of one group
        cap = (len(data.y_list) - data.groups.value_counts().max()) * 3 / 4

        n_neigh_values = np.linspace(floor, cap, 50, dtype=np.int64).tolist()

        self.parameters = {'n_neighbors': n_neigh_values,
                           'leaf_size': self.leaf_size_values,
                           'weights': ['uniform'],
                           'algorithm': self.algorithm_values,
                           'metric': ['manhattan'],
                           }

    def param_search(self, test=False):
        if test:
            self.parameters = {}

        knn = KNeighborsClassifier()
        logo = LeaveOneGroupOut()

        clf = GridSearchCV(estimator=knn,
                           param_grid=self.parameters,
                           scoring='roc_auc_ovo_weighted',
                           cv=logo.split(X=self.data.X_list, groups=self.data.groups),
                           verbose=51,
                           n_jobs=threads,
                           pre_dispatch='n_jobs'
                           )
        clf.fit(self.data.X_list, self.data.y_list)

        return clf
