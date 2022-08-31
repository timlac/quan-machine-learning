import numpy as np
import h5py
import os

from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.model_selection import LeaveOneGroupOut

from global_config import ROOT_DIR


class ConfusionMatrixCreator:

    def __init__(self, x, y, groups, model_parameters):
        """
        :param x: np.array
        :param y: np.array
        :param groups: np.array
        :param model_parameters: dict
        """
        self.x = x
        self.y = y
        self.groups = groups
        self.model_parameters = model_parameters

        self.classes = np.unique(self.y)
        self.n_classes = len(self.classes)

    def create_split(self):
        logo = LeaveOneGroupOut()
        cv = logo.split(X=self.x, groups=self.groups)
        return cv

    def load_classifier(self):
        clf = SVC(**self.model_parameters)
        return clf

    def calculate_avg_conf_matrix(self):
        clf = self.load_classifier()
        cv = self.create_split()
        cum_conf_mat = np.zeros([self.n_classes, self.n_classes])

        n_groups = 0
        for train_idx, val_idx in cv:
            n_groups += 1
            x_train, x_val, y_train, y_val = self.x[train_idx], self.x[val_idx], self.y[train_idx], self.y[val_idx]

            clf.fit(x_train, y_train)
            y_pred = clf.predict(x_val)
            conf_mat = confusion_matrix(y_val,
                                        y_pred,
                                        labels=self.classes,
                                        normalize='true'
                                        )

            cum_conf_mat += conf_mat

        avg_conf_mat = cum_conf_mat / n_groups
        return avg_conf_mat


def main():

    input_path = os.path.join(ROOT_DIR, 'files/out/functionals/video_data_functionals_A220.hdf5')

    f = h5py.File(input_path, 'r')
    _x = np.array(f['x'])
    y = np.array(f['y'])
    groups = np.array(f['groups'])
    for k in f.attrs.keys():
        print(f"{k} : {f.attrs[k]}")

    scaler = MinMaxScaler()
    x = scaler.fit_transform(_x)
    x, y, groups = shuffle(x, y, groups)

    model_parameters = {"kernel": "linear"}

    conf_mat_creator = ConfusionMatrixCreator(x, y, groups, model_parameters)
    conf_mat = conf_mat_creator.calculate_avg_conf_matrix()

    print(conf_mat)


if __name__ == "__main__":
    main()
