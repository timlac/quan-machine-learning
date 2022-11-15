import torch
from torch.nn.utils.rnn import pad_sequence
import pandas as pd
import numpy as np


def get_padded_time_series_with_torch(slices, X_COLS=None, padding_value=-1000):
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