import numpy as np


# TODO: Since some videos are removed in this step the sync between openface and opensmile data will need to be monitored


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

        removed = 0
        interpolated = 0
        processed = 0
        for df in slices:
            processed += 1

            confidence = df[self.CONFIDENCE].values
            success = df[self.SUCCESS].values

            n_rows = df.shape[0]
            ratio_high_conf = (confidence > self.CONFIDENCE_THRESHOLD).sum() / n_rows
            ratio_successful = (success == self.SUCCESS_INDICATOR).sum() / n_rows

            if ratio_successful < 1 or ratio_high_conf < 1:
                if ratio_successful < self.MIN_RATIO_GOOD_FRAMES or ratio_high_conf < self.MIN_RATIO_GOOD_FRAMES:
                    # skip dataframes with too many bad values
                    removed += 1
                    continue
                else:
                    # interpolate if not too many values are bad
                    interpolated += 1
                    df = self.interpolate(df)
                    ret.append(df)
            else:
                # just append if no values are bad
                ret.append(df)

        print("a total of {} videos were processed". format(processed))

        print("{} videos had over {} bad frames and were therefore completely removed"
              .format(removed, self.MIN_RATIO_GOOD_FRAMES))
        print("{} videos had some bad frames and underwent interpolation"
              .format(interpolated))

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




# import os
# import pandas as pd
# from global_config import ROOT_DIR
# from src.preprocessing.dataset_creation.helpers import slice_by
# path = os.path.join(ROOT_DIR, "files/out/openface_query.csv")
# df = pd.read_csv(path)
# slices = slice_by(df, "filename")
#
# print("before interpolation")
# print(len(slices))
#
#
# from global_config import AU_INTENSITY_COLS
# interpolator = Interpolator(AU_INTENSITY_COLS)
# interpolated_slices = interpolator.remove_interpolate(slices)
#
# print("after interpolation")
# print(len(interpolated_slices))