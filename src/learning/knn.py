from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_validate
import numpy as np
import sys

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import GridSearchCV

from src.global_config import *
from src.learning.load_data import DataLoader
from src.learning.save_output import Saver
import time

# get the start time
st = time.time()

print("running knn")
print("input file: " + sys.argv[1])
print("save location: " + sys.argv[2])

data = DataLoader(filename=sys.argv[1])

# we want to evaluate different number of neighbors (clusters) based on the size of the training set.
# set a cluster floor at the number of targets
floor = len(data.y.unique())
# set a cluster cap equal to 3/4:ths of the size of the training set.
# size of training set is equal to all datapoints minus the size of one group
cap = (len(data.y) - data.groups.value_counts().max()) * 3 / 4

n_neigh_values = np.linspace(floor, cap, 50, dtype=np.int64).tolist()

# Define other to evaluate
leaf_size_values = [10, 20, 30]
algorithm_values = ['ball_tree', 'brute', 'kd_tree']
parameters = {'n_neighbors': n_neigh_values,
              'leaf_size': leaf_size_values,
              'weights': ['uniform'],
              'algorithm': algorithm_values,
              'metric': ['manhattan'],
              'n_jobs': [-1]
              }

parameters = {}


knn = KNeighborsClassifier()
logo = LeaveOneGroupOut()

clf = GridSearchCV(estimator=knn,
                   param_grid=parameters,
                   scoring='roc_auc_ovo_weighted',
                   cv=logo.split(X=data.X, groups=data.groups),
                   verbose=51,
                   n_jobs=threads,
                   pre_dispatch='n_jobs'
                   )
clf.fit(data.X, data.y)

saver = Saver(clf=clf, method="knn", n_groups=data.n_groups, save_location=sys.argv[2])
saver.save()

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')