from sklearn.tree import DecisionTreeClassifier
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

print("running decision tree")
print("input file: " + sys.argv[1])
print("save location: " + sys.argv[2])

data = DataLoader(filename=sys.argv[1])

# Define parameters to evaluate
criterion_values = ['gini', 'entropy']
splitter_values = ['best', 'random']
max_depth_values = np.arange(5, 55, 5).tolist()
min_samples_split_values = np.linspace(0.1, 1.0, 10, endpoint=True)
min_samples_leaf_values = np.linspace(0.1, 0.5, 5, endpoint=True)
max_features_values = [int(x) for x in np.linspace(1, len(data.X.columns), num=18)]  # list(range(1,len(X.columns)))


parameters = {'criterion': criterion_values,
              'splitter': splitter_values,
              'max_depth': max_depth_values,
              'min_samples_split': min_samples_split_values,
              'min_samples_leaf': min_samples_leaf_values,
              'max_features': max_features_values,
              'class_weight': ['balanced'],
              'random_state': [seed]
              }


dt = DecisionTreeClassifier()
logo = LeaveOneGroupOut()

# Reduce the number of possible combinations by randomly resampling to 5000 combinations
clf = RandomizedSearchCV(estimator=dt,
                         param_distributions=parameters,
                         scoring='roc_auc_ovo_weighted',
                         cv=logo.split(X=data.X, groups=data.groups),
                         verbose=51,
                         random_state=seed,
                         n_iter=5000,
                         n_jobs=threads,
                         pre_dispatch='n_jobs'
                         )
clf.fit(data.X, data.y)
print(clf.best_estimator_)

saver = Saver(clf=clf, method="tree", n_groups=data.n_groups, save_location=sys.argv[2])
saver.save()

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')