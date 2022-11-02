import os
import pandas as pd
import numpy as np
import scipy
from src.preprocessing.dataset_creation.time_series_handling import pad_list_of_series, time_series_to_list
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, TARGET_COLUMN
from src.preprocessing.sql_handling.queries import query_au_cols_without_confidence_filter_A220


def query_to_list(query):
    # df, _ = execute_sql_pandas(query)
    df = pd.read_csv(ROOT_DIR + "/files/out/au_cols_a74.csv")

    slices = slice_by("filename", df)
    slices = remove_interpolate(slices)
    functionals = calculate_aggregate_measures(slices)


def calculate_aggregate_measures(slices):
    ret = []
    for df in slices:

        x = df[AU_INTENSITY_COLS].values

        m = np.mean(x, axis=0)
        per20 = np.percentile(x, 20, axis=0)
        per50 = np.percentile(x, 50, axis=0)
        per80 = np.percentile(x, 80, axis=0)
        iqr2080 = scipy.stats.iqr(x, rng=(20, 80), axis=0)

        ret = None
        for i in range(len(AU_INTENSITY_COLS)):
            temp = np.concatenate((m[i], per20[i], per50[i], per80[i], iqr2080[i]), axis=None)
            if ret is None:
                ret = temp
            else:
                ret = np.concatenate((ret, temp), axis=None)

        x = np.nan_to_num(x)

    return ret


def remove_interpolate(slices):
    threshold = 0.85

    ret = []

    for df in slices:

        confidence = df["confidence"].values
        success = df["success"].values

        n_rows = df.shape[0]
        ratio_high_conf = (confidence > 0.98).sum() / n_rows
        ratio_successful = (success == 1).sum() / n_rows

        if ratio_successful < 1 or ratio_high_conf < 1:
            if ratio_successful < threshold or ratio_high_conf < threshold:
                continue
            else:
                df = interpolate(df)
                ret.append(df)
        else:
            ret.append(df)

    return ret


def interpolate(df):
    # set the AU value of all rows with bad values to NaN
    for x in AU_INTENSITY_COLS:
        df.loc[(df["success"] != 1) | (df["confidence"] != 1), x] = np.NaN

    # interpolate
    df[AU_INTENSITY_COLS] = df[AU_INTENSITY_COLS].interpolate(method="linear")

    # drop rows that couldn't be interpolated
    df = df.dropna()

    return df


def slice_by(identifier, df):
    ret = []
    for _, group in df.groupby(identifier):
        ret.append(group)
    return ret


query_to_list(None)
