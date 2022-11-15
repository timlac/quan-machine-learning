import numpy as np
import pandas as pd
import os
from global_config import ROOT_DIR, AU_INTENSITY_COLS


def time_series_to_list(df, identifier, x_cols, y_col):
    """
    :param df: pd.Dataframe
    :param identifier: which column to split time series by
    :param x_cols: column names for input features
    :param y_col: column name for labels
    :return: tuple of lists: x length = number of time series and every element of shape (number of frames, number of features)
                            y length = number of time series
    """
    x = []
    y = []
    for _, group in df.groupby(identifier):
        x_arr = np.array(group[x_cols].values)
        x.append(x_arr)

        y_val = group[[y_col]].values[0][0]
        y.append(y_val)

    return x, y


def pad_list_of_series(ts_list, padding_value=-1000):
    """
    :param ts_list: a list of time series where every element has shape (number of frames, number of features)
    :return: np.array where every element in the series has been padded with zeros and then transformed into a matrix
                with shape (number of observations, number of frames, number of features)
    """
    # obtain the longest element in the list
    max_length = max(map(len, ts_list))

    padded_list = []
    for series in ts_list:

        diff = max_length - len(series)

        # create an empty np array of appropriate size
        pad = np.full(shape=(diff, series.shape[1]), fill_value=padding_value)

        # concat with series and transpose in order to
        series = np.concatenate((series, pad))

        padded_list.append(series)

    return np.asarray(padded_list)


def main():
    pass
    # load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data.csv")
    # df = pd.read_csv(load, nrows=10000)
    # x, y, video_ids = time_series_to_list(df, "filename", AU_INTENSITY_COLS, "emotion_1_id", "video_id")

    # padded_x = pad_list_of_series(x)
    #
    # out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/padded_time_series.npz")
    # np.savez(out, x=padded_x, y=y)


if __name__ == "__main__":
    main()