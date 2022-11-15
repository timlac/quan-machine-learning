import numpy as np
import pandas as pd


def get_padded_time_series_with_numpy(ts_list, padding_value=-1000):
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


def get_cols(slices, COLS):
    ret = []
    for df in slices:
        array = df[COLS].values
        ret.append(array)
    return ret


def get_fixed_col(slices, COL_NAME):
    """
    :param slices: list of dataframes
    :param COL_NAME: column name
    :return: np array with the extracted column value, one for each dataframe
    """
    y = []
    for df in slices:
        array = df[COL_NAME].values
        if len(np.unique(array)) != 1:
            raise ValueError("something went wrong, more than one {} found for time series".format(COL_NAME))
        else:
            y.append(array[0])
    return np.asarray(y)


def slice_by(df, identifier):
    """
    :param df: dataframe with multiple time series
    :param identifier: column name to identify unique time series
    :return: list of dataframes
    """
    ret = []
    for _, group in df.groupby(identifier):
        ret.append(group)
    return ret
