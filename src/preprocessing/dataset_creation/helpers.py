import numpy as np
import pandas as pd
import os
from global_config import ROOT_DIR, AU_INTENSITY_COLS, video_id_to_fps

from itertools import compress


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


def filter_by_video_id(slices, video_ids, video_id_filter):
    boolean_indices = np.in1d(video_ids, video_id_filter)
    slice_to_keep = list(compress(slices, boolean_indices))
    return slice_to_keep


def main():
    df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/query.csv"))

    slices = slice_by(df, "filename")

    au = get_cols(slices, AU_INTENSITY_COLS)
    video_ids = get_fixed_col(slices, "video_id")

    fps_50_video_ids = []
    for key, value in video_id_to_fps.items():
        if value == 50:
            fps_50_video_ids.append(key)
    fps_50_video_ids = np.array(fps_50_video_ids)

    fps_25_video_ids = []
    for key, value in video_id_to_fps.items():
        if value == 25:
            fps_25_video_ids.append(key)

    for v in fps_25_video_ids:
        if v in video_ids:
            print("video {} has 25 FPS".format(v))

    for i in np.unique(video_ids):
        print(i)

    # filter_by_video_id(au, video_ids, fps_50_video_ids)


if __name__ == "__main__":
    main()
