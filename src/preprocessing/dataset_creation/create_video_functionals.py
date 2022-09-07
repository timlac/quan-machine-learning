from scipy.signal import find_peaks
import pandas as pd
from global_config import ROOT_DIR
import os
import numpy as np
import scipy


def my_find_peaks(x):
    """
    This function takes a 1-D array and finds all local maxima by simple comparison of neighboring values.
    Optionally, a subset of these peaks can be selected by specifying conditions for a peak’s properties.
    """
    th = x.mean()
    val = x.values
    peaks, _ = scipy.signal.find_peaks(val, height=th)
    return len(peaks)


def calculate_means(df):
    df = df.groupby(['filename']).agg(['mean']).sort_values(by=['filename'], ignore_index=True)

    # Impute NaN values
    # There might be some NaN values in the dataframe
    # coming from the coefficient of variation (std(x)/mean(x) when mean(x)=0)
    df.fillna(0, inplace=True)

    # Collapse hierarchical index in columns
    df.columns = ['_'.join(col).strip('_') for col in df.columns.values]

    # check for null values
    if df.isnull().values.any():
        raise ValueError

    return df


def calculate_aggregate_measures(df):
    # Compute statistical measures
    # Coefficient of variation
    # 20th percentile, i.e. below this value 20% of the observations will be found
    # 50th percentile, i.e. below this value 50% of the observations will be found
    # 80th percentile, i.e. below this value 80% of the observations will be found
    # IQR(60%) = 80th percentile - 20th percentile
    # Number of peaks above the adaptive threshold

    df = df.groupby(['filename']).agg(['mean',  # Arithmetic mean
                                       lambda x: scipy.stats.variation(x),
                                       lambda x: np.percentile(x, q=20),
                                       lambda x: np.percentile(x, q=50),
                                       lambda x: np.percentile(x, q=80),
                                       lambda x: scipy.stats.iqr(x, rng=(20, 80)),
                                       lambda x: my_find_peaks(x),
                                       ]).reset_index().sort_values(by=['filename'], ignore_index=True)

    # Rename columns
    df.rename(columns={'<lambda_0>': 'stddevNorm',
                       '<lambda_1>': 'percentile20.0',
                       '<lambda_2>': 'percentile50.0',
                       '<lambda_3>': 'percentile80.0',
                       '<lambda_4>': 'iqr60_80-20',
                       '<lambda_5>': 'numPeaks',
                       }, level=1, inplace=True)

    # Impute NaN values
    # There might be some NaN values in the dataframe
    # coming from the coefficient of variation (std(x)/mean(x) when mean(x)=0)
    df.fillna(0, inplace=True)

    # Collapse hierarchical index in columns
    df.columns = ['_'.join(col).strip('_') for col in df.columns.values]

    # check for null values
    if df.isnull().values.any():
        raise ValueError

    return df


def create_functionals(df):
    # get the metadata from original dataframe
    df_metadata = df[["filename", "video_id", "emotion_1_id"]]

    # drop all duplicate rows, will collapse dataframe to unique filenames
    df_metadata = df_metadata.drop_duplicates()

    df = df.drop(columns=["video_id", "emotion_1_id"])

    df = calculate_aggregate_measures(df)

    # merge metadata with temporary dataframe
    df = pd.merge(df, df_metadata, on="filename")

    return df


def main():
    load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data.csv")
    df = pd.read_csv(load, nrows=10000)
    df = create_functionals(df)
    print(df)


if __name__ == "__main__":
    pass