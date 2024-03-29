from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import GridSearchCV
from global_config import seed
from sklearn.svm import SVC
import os
import argparse
import h5py
import time
import datetime

from src.analysis.supervised_learning.param_search.save_output import Saver
from src.analysis.supervised_learning.param_search.load_data import DataLoader
from global_config import ROOT_DIR
from constants import CONSTANTS


class SVM:
    # Define parameters to evaluate
    # defining parameter range
    c_values = [0.1, 1, 10, 100, 1000]
    gamma = [1, 0.1, 0.01, 0.001, 0.0001]
    kernel = ['rbf', 'linear', 'poly', 'sigmoid']

    parameters = {'class_weight': ['balanced'],
                  'random_state': [seed],
                  'C': c_values,
                  'gamma': gamma,
                  'kernel': kernel,
                  }

    @classmethod
    def param_search(cls, data, test=False):
        if test:
            cls.parameters = {}

        svc = SVC()
        logo = LeaveOneGroupOut()

        clf = GridSearchCV(estimator=svc,
                           param_grid=cls.parameters,
                           scoring='accuracy',
                           cv=logo.split(X=data.x, groups=data.groups),
                           verbose=51,
                           n_jobs=-1,
                           )

        clf.fit(data.x, data.y)
        return clf


def main():
    input_path = os.path.join(ROOT_DIR, "files/out/functionals/video_data_functionals.hdf5")
    output_path = os.path.join(ROOT_DIR, "files/out/functionals/supervised_learning/video/grid_search/")
    output_filename = "au_functionals"

    parser = argparse.ArgumentParser()
    parser.add_argument("group_type", choices=[CONSTANTS.TWINNED, CONSTANTS.VIDEO_ID])
    args = parser.parse_args()
    group_type = args.group_type

    data = DataLoader(input_path, group_type)

    # get the start time
    st = time.time()
    print("starting at time: " + str(datetime.datetime.now()))

    clf = SVM.param_search(data)

    # get the end time
    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print('Execution time:', str(datetime.timedelta(seconds=elapsed_time)))

    saver = Saver(clf=clf, method="svm", group_type=group_type, n_groups=data.n_groups, save_location=output_path, filename=output_filename)
    saver.save()


if __name__ == "__main__":
    main()
