import pandas as pd
from global_config import AU_INTENSITY_COLS
import numpy as np
import os

from global_config import ROOT_DIR


class MissingTimeSeriesValuesHandler:

    # constants for SQL/df column names
    SLICE_BY = "filename"
    CONFIDENCE = "confidence"
    SUCCESS = "success"

    def __init__(self, threshold=0.9):
        self.threshold = threshold
        self.interpolation_candidates = []

    def remove_and_interpolate(self, df):
        df = self.remove_unsuccessful(df)
        df = self.interpolate(df)
        return df

    def remove_unsuccessful(self, df):
        filenames_to_remove = []

        # iterate over a df for every filename
        for filename, df_filename in df.groupby(self.SLICE_BY):
            # get the total number of frames
            total = df_filename.shape[0]

            # get the sum of all rows with success and greater than 0.98 confidence in df
            successful = (df_filename[self.SUCCESS] == 1).sum()
            confident = (df_filename[self.CONFIDENCE] > 0.98).sum()

            # calculate ratio between unsuccessful or low confidence rows and total number of rows
            success_ratio = successful / total
            confidence_ratio = confident / total

            if success_ratio < 1 or confidence_ratio < 1:
                if success_ratio < self.threshold or confidence_ratio < self.threshold:
                    filenames_to_remove.append(filename)
                else:
                    self.interpolation_candidates.append(filename)

        df = df[df.filename.isin(filenames_to_remove) == False]

        return df

    def interpolate(self, df):
        """
        :param df: the dataframe to be interpolated
        :param filenames_to_interpolate: filenames, e.g. time series that will undergo interpolation
        :return: the full dataframe with the selected time series interpolated
        """
        # set the AU value of all rows with bad frames to NaN
        for au in AU_INTENSITY_COLS:
            df.loc[(df[self.SUCCESS] != 1) | (df[self.CONFIDENCE] != 1), au] = np.NaN

        for filename in self.interpolation_candidates:
            # select dataframe subset
            df_filename = df[df[self.SLICE_BY] == filename]

            # interpolate
            df_filename[AU_INTENSITY_COLS] = df_filename[AU_INTENSITY_COLS].interpolate(method="linear")

            # set subset to the interpolated frame
            df[df[self.SLICE_BY] == filename] = df_filename

        # drop rows that couldn't be interpolated
        df = df.dropna()

        return df


def main():
    load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data_with_unsuccessful.csv")
    df = pd.read_csv(load, nrows=100000)
    m = MissingTimeSeriesValuesHandler()

    df = m.remove_unsuccessful(df)
    df = m.interpolate(df)

    print("hej")


if __name__ == "__main__":
    main()
