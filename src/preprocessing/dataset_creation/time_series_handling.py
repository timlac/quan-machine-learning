import numpy as np
import pandas as pd
import os
from global_config import ROOT_DIR, AU_INTENSITY_COLS
import torch

#
# class ListedData:
#
#     def __init__(self):
#         self.x = []
#         self.y = []
#         self.video_ids = []
#         self.filenames = []
#
#


def time_series_to_list(df, identifier, x_cols, y_col, video_id_col):
    """
    :param df: pd.Dataframe
    :param identifier: which column to split time series by
    :param x_cols: column names for input features
    :param y_col: column name for labels
    :return: list with length = number of time series and every element of shape (number of frames, number of features)
    """
    x = []
    y = []
    video_ids = []
    for _, group in df.groupby(identifier):
        x_arr = torch.Tensor(group[x_cols].values)
        x.append(x_arr)

        y_val = group[[y_col]].values[0][0]
        y.append(y_val)

    return x, y


def pad_list_of_series(ts_list):
    """
    :param ts_list: a list of time series where every element has shape (number of frames, number of features)
    :return: np.array where every element in the series has been padded with zeros and then transformed into a matrix
                with shape (number of observations, number of frames, number of features)
    """
    # obtain the longest element in the list
    length = max(map(len, ts_list))

    padded_list = []
    for series in ts_list:
        # create an empty np array of appropriate size
        pad = np.zeros((length-len(series), series.shape[1]))

        # concat with series and transpose in order to
        series = np.concatenate((series, pad))

        padded_list.append(series)

    return np.asarray(padded_list)


def main():
    load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data.csv")
    df = pd.read_csv(load, nrows=10000)
    x, y, video_ids = time_series_to_list(df, "filename", AU_INTENSITY_COLS, "emotion_1_id", "video_id")

    # padded_x = pad_list_of_series(x)
    #
    # out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/padded_time_series.npz")
    # np.savez(out, x=padded_x, y=y)


if __name__ == "__main__":
    main()






# length = max(map(len, X_list))
#
# padded_X = []
# for xi in X_list:
#     pad = np.zeros((length-len(xi), xi.shape[1]))
#     xi = np.concatenate((xi, pad)).T
#     padded_X.append(xi)
#
# X = np.asarray(padded_X)