import numpy as np
import torch
from torch.nn.utils.rnn import pad_sequence
import pandas as pd


def get_padded_time_series(slices, X_COLS=None, padding_value=-1000):
    """
    :param padding_value: the value to pad the time series with
    :param slices: list of dataframes or numpy arrays
    :return: np array
    """
    x_list = []
    for sli in slices:
        if isinstance(sli, pd.DataFrame):
            x = sli[X_COLS].values
        elif isinstance(sli, np.ndarray):
            x = sli
        else:
            raise Exception("slice not pandas dataframe or numpy array")

        x_tensor = torch.Tensor(x)
        x_list.append(x_tensor)

    ret = pad_sequence(x_list, batch_first=True, padding_value=padding_value)
    return np.asarray(ret)


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
