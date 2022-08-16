import pandas as pd
from global_config import AU_INTENSITY_COLS
import numpy as np
import os

from global_config import ROOT_DIR


class MissingTimeSeriesValuesHandler:

    def __init__(self, threshold=0.9):
        self.threshold = threshold
        self.interpolation_candidates = []

    def remove_unsuccessful(self, df):
        filenames_to_remove = []

        # iterate over a df for every filename
        for filename, df_filename in df.groupby('filename'):
            # get the total number of frames
            total = df_filename.shape[0]

            # get the sum of all rows with success and greater than 0.98 confidence in df
            successful = (df_filename['success'] == 1).sum()
            confident = (df_filename['confidence'] > 0.98).sum()

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
            df.loc[(df['success'] != 1) | (df['confidence'] != 1), au] = np.NaN

        for filename in self.interpolation_candidates:
            # select dataframe subset
            df_filename = df[df['filename'] == filename]

            # interpolate
            df_filename[AU_INTENSITY_COLS] = df_filename[AU_INTENSITY_COLS].interpolate(method="linear")

            # set subset to the interpolated frame
            df[df['filename'] == filename] = df_filename

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
