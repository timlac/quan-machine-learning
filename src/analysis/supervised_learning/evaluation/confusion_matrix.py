import numpy as np
import h5py
import os

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.model_selection import LeaveOneGroupOut

from sklearn.model_selection import KFold
import seaborn as sns


from global_config import ROOT_DIR, AU_INTENSITY_COLS, emotion_id_to_emotion_abr, conf_cmap
from src.preprocessing.dataset_creation.aggregation import get_aggregate_measures
from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col
from src.utils.helpers import mapper


class ConfusionMatrixCreator:

    def __init__(self, x, y, model_parameters):
        """
        :param x: np.array
        :param y: np.array
        :param model_parameters: dict
        """
        self.x = x
        self.y = y
        self.model_parameters = model_parameters

        self.classes = np.unique(self.y)
        self.n_classes = len(self.classes)

    def load_classifier(self):
        clf = SVC(**self.model_parameters)
        return clf

    def calculate_avg_conf_matrix(self, cv):
        clf = self.load_classifier()
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


def plot_conf_matrix(df_cm, title):
    plt.figure(figsize=(20, 15))
    ax = sns.heatmap(df_cm, annot=True, fmt='.2f', vmin=0, vmax=1, cmap=conf_cmap)
    plt.yticks(va='center')
    plt.xlabel('Predicted Label')
    plt.ylabel('Actual Label')
    plt.title(title)
    plt.show()


def main():
    df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/openface_query_A220.csv"))

    slices = slice_by(df, "filename")

    x = get_cols(slices, AU_INTENSITY_COLS)
    x = get_aggregate_measures(x,
                                    means=True,
                                    variance=False,
                                    deltas=False,
                                    peaks=False)
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)

    y = get_fixed_col(slices, "emotion_1_id")
    params = {'C': 50, 'class_weight': 'balanced', 'gamma': 1, 'kernel': 'rbf'}

    skf = KFold(n_splits=5, shuffle=True)
    cv = skf.split(x, y)

    c = ConfusionMatrixCreator(x, y, params)
    conf_mat = c.calculate_avg_conf_matrix(cv)

    # get emotion_ids
    emotion_ids = np.unique(y)

    # get emotion abreviations
    emotion_abrs = mapper(emotion_ids, emotion_id_to_emotion_abr)

    # create dataframe with lists of emotion ids as row and column names
    df_cm = pd.DataFrame(conf_mat, list(emotion_abrs), list(emotion_abrs))

    plot_conf_matrix(df_cm, 'SVM Normalized Confusion Matrix')


if __name__ == "__main__":
    main()
