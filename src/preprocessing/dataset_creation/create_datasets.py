import os
import pandas as pd
import numpy as np
import scipy
from src.preprocessing.dataset_creation.time_series_handling import pad_list_of_series, time_series_to_list
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, TARGET_COLUMN
from src.preprocessing.sql_handling.queries import query_au_cols_without_confidence_filter_A220, query_au_cols_without_confidence_filter, query_au_cols_without_confidence_filter_A74


def create_ds(query, save_as, X_COLS):
    df, _ = execute_sql_pandas(query)
    # df = pd.read_csv(ROOT_DIR + "/files/out/au_cols_a74.csv")

    slices = slice_by("filename", df)

    interpolator = Interpolator(X_COLS)
    slices = interpolator.remove_interpolate(slices)

    x = calculate_aggregate_measures(slices, X_COLS)
    y = get_y(slices)

    print(x.shape)
    print(y.shape)

    np.savez_compressed(save_as, x=x, y=y)


def calculate_aggregate_measures(slices, X_COLS):
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


class Interpolator:

    # parameters
    MIN_RATIO_GOOD_FRAMES = 0.85
    CONFIDENCE_THRESHOLD = 0.98
    SUCCESS_INDICATOR = 1

    # string constants
    CONFIDENCE = "confidence"
    SUCCESS = "success"
    INTERPOLATION_METHOD = "linear"

    def __init__(self, X_COLS):
        """
        :param X_COLS: the columns to be interpolated
        """
        self.X_COLS = X_COLS

    def remove_interpolate(self, slices):
        """
        :param slices: list of dataframes to interpolate bad values for (must contain confidence and success columns
                        as well as X_COLS
        :return: list of dataframes with interpolated values
        """

        ret = []

        for df in slices:

            confidence = df[self.CONFIDENCE].values
            success = df[self.SUCCESS].values

            n_rows = df.shape[0]
            ratio_high_conf = (confidence > self.CONFIDENCE_THRESHOLD).sum() / n_rows
            ratio_successful = (success == self.SUCCESS_INDICATOR).sum() / n_rows

            if ratio_successful < 1 or ratio_high_conf < 1:
                if ratio_successful < self.MIN_RATIO_GOOD_FRAMES or ratio_high_conf < self.MIN_RATIO_GOOD_FRAMES:
                    # skip dataframes with too many bad values
                    continue
                else:
                    # interpolate if not too many values are bad
                    df = self.interpolate(df)
                    ret.append(df)
            else:
                # just append if no values are bad
                ret.append(df)

        return ret

    def interpolate(self, df):
        """
        :param df: pandas Dataframe to interpolate
        :return:
        """
        # iterate over X_cols and set cells with bad values to NaN
        for x in self.X_COLS:
            df.loc[(df[self.SUCCESS] != 1) | (df[self.CONFIDENCE] != 1), x] = np.NaN

        # interpolate
        df[self.X_COLS] = df[self.X_COLS].interpolate(method=self.INTERPOLATION_METHOD)

        # drop rows that couldn't be interpolated
        df = df.dropna()

        return df


def get_y(slices):
    y = []
    for df in slices:
        array = df["emotion_1_id"].values
        if len(np.unique(array)) != 1:
            raise ValueError("something went wrong, more than one emotion id found for time series")
        else:
            y.append(array[0])
    return np.asarray(y)


def slice_by(identifier, df):
    ret = []
    for _, group in df.groupby(identifier):
        ret.append(group)
    return ret


def main():
    out = os.path.join(ROOT_DIR, "files/out/functionals/video_data_functionals_A74.npz")
    create_ds(query_au_cols_without_confidence_filter_A74, out)


if __name__ == "__main__":
    main()
