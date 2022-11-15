import pickle

import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
from scipy.stats import variation, iqr

from scipy.signal import find_peaks
import pandas as pd
import os

from sklearn.preprocessing import StandardScaler

from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS
from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col, get_padded_time_series


def my_find_peaks(x):
    """
    This function takes a 1-D array and finds all local maxima by simple comparison of neighboring values.
    Optionally, a subset of these peaks can be selected by specifying conditions for a peak’s properties.
    """
    # only look at peaks above mean value
    th = np.mean(x)
    peaks, _ = find_peaks(x, height=th)
    return len(peaks)


def check_for_nan(arr):
    # Check if the NumPy array contains any NaN value
    if np.isnan(arr).any():
        print("The Array contain NaN values")
    else:
        print("The Array does not contain NaN values")


def get_aggregate_measures(slices,
                           means=True,
                           variance=True,
                           deltas=True,
                           peaks=True):
    """
    :param slices: list of numpy arrays
    :return: np array with mean values and other aggregate measures
    """
    ret = []
    for sli in slices:
        measures = []

        if means:
            measures.extend([np.mean(sli, axis=0),
                             np.percentile(sli, 20, axis=0),
                             np.percentile(sli, 50, axis=0),
                             np.percentile(sli, 80, axis=0),
                             iqr(sli, rng=(20, 80), axis=0)])

        if variance:
            measures.append(np.var(sli, axis=0))

        if deltas or peaks:
            sli = smooth(sli)
            if deltas:
                d_mean, d_std = delta(sli)
                measures.extend([d_mean, d_std])
            if peaks:
                p = np.apply_along_axis(my_find_peaks, 0, sli)
                measures.append(p)

        # stack columns
        stacked_aggregates = np.hstack(measures)

        # check_for_nan(stacked_aggregates)
        stacked_aggregates = np.nan_to_num(stacked_aggregates)
        # check_for_nan(stacked_aggregates)

        ret.append(stacked_aggregates)

    arr = np.asarray(ret)

    return arr


def moving_average(x, w=3):
    """
    :param x: np array with a one dimensional time series
    :param w: window size
    :return: smoothed np array
    """
    return np.convolve(x, np.ones(w), 'valid') / w


def smooth(ts):
    """
    :param ts: np array with (rows = time steps) and (cols = features).
    :return: mean and std of delta
    """
    x_smooth = np.apply_along_axis(moving_average, 0, ts)
    return x_smooth


def delta(ts):
    """
    :param ts: np array with (rows = time steps) and (cols = features)
    :return: mean and std of delta
    """
    deltas = np.diff(ts, axis=0)

    deltas_masked = ma.masked_where(deltas == 0, deltas)

    mean = np.mean(deltas_masked, axis=0)
    std = np.std(deltas_masked, axis=0)

    return mean, std


def normalize(ts):
    """
    :param ts: np array with (rows = time steps) and (cols = features)
    :return: scaled np array
    """
    scaler = StandardScaler()
    scaler.fit(ts)
    ret = scaler.transform(ts)
    return ret


from src.analysis.data_exploration import plot_time_series_means, plot_means

with open(os.path.join(ROOT_DIR, "files/out/data.pickle"), "rb") as input_file:
    file = pickle.load(input_file)

x = file['x']
y = file['y']

au = x['au']
gaze = x['gaze']
pose = x['pose']

# plot_time_series_means(get_padded_time_series(au), y, AU_INTENSITY_COLS)
au_agg = get_aggregate_measures(au)
plot_means(au_agg, y, AU_INTENSITY_COLS)
