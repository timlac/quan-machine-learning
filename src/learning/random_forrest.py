from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
import numpy as np
import sys

from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import RandomizedSearchCV

from src.global_config import *
from src.learning.load_data import DataLoader
from src.learning.save_output import Saver

import time

# get the start time
st = time.time()

print("running random forrest")
print("input file: " + sys.argv[1])
print("save location: " + sys.argv[2])

data = DataLoader(filename=sys.argv[1])

# Define parameters to evaluate
# the number of trees to build before taking the maximum voting or averages of predictions
n_estimators_values = [int(x) for x in np.linspace(10, 1000, num=50)]  # np.arange(100, 810, 10).tolist()
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


rf = RandomForestClassifier()
logo = LeaveOneGroupOut()

# Reduce the number of possible combinations by randomly resampling to 5000 combinations
clf = RandomizedSearchCV(estimator=rf,
                         param_distributions=parameters,
                         scoring='roc_auc_ovo_weighted',
                         cv=logo.split(X=data.X, groups=data.groups),
                         verbose=51,
                         n_iter=5000,
                         random_state=seed,
                         n_jobs=-25,
                         pre_dispatch='n_jobs'
                         )
clf.fit(data.X, data.y)

saver = Saver(clf=clf, method="rf", n_groups=data.n_groups, save_location=sys.argv[2])
saver.save()

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')