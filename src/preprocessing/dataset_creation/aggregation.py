import numpy as np
import scipy


def get_aggregate_measures(slices, X_COLS):
    """
    :param slices: list of dataframes
    :param X_COLS: list of column names for x
    :return: np array with mean values and other aggregate measures
    """
    ret = []
    for df in slices:
        x = df[X_COLS].values

        m = np.mean(x, axis=0)
        per20 = np.percentile(x, 20, axis=0)
        per50 = np.percentile(x, 50, axis=0)
        per80 = np.percentile(x, 80, axis=0)
        iqr2080 = scipy.stats.iqr(x, rng=(20, 80), axis=0)

        x = np.concatenate((m, per20, per50, per80, iqr2080), axis=None)

        x = np.nan_to_num(x)
        ret.append(x)

    arr = np.asarray(ret)

    return arr
