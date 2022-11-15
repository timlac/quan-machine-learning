import os
import numpy as np
import pandas as pd
from itertools import compress
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pickle

from src.utils.helpers import list2string
from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col
from src.preprocessing.dataset_creation.aggregation import get_aggregate_measures
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS
from src.preprocessing.dataset_creation.interpolation import Interpolator

from src.preprocessing.dataset_creation.aggregation import smooth, normalize


class XData:

    def __init__(self, au, gaze, pose):
        self.au = au
        self.gaze = gaze
        self.pose = pose


class Dataset:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class DatasetCreator:

    X_COLS = [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS]

    # padding value for time series datasets
    # variable length time series requires padding to create an array with same length rows
    PADDING_VALUE = -1000

    query = """SELECT filename,
                    video_id,
                    emotion_1_id,
                    success,
                    confidence,
                    `{X_COLS}`
                    FROM openface
                    WHERE mix = 0
                    AND intensity_level in (2,3)
                    AND mode = 'p';""".format(X_COLS=list2string(X_COLS))

    def __init__(self,
                 aggregate=True):

        # aggregate (create functionals) or not (only applicable for openface features
        self.aggregate = aggregate

    def create(self):
        # df, _ = execute_sql_pandas(query)
        # df.to_csv(os.path.join(ROOT_DIR, "files/out/query.csv"), index=False)

        df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/query.csv"))

        slices = slice_by(df, "filename")
        slices = self.interpolate(slices)

        au = get_cols(slices, AU_INTENSITY_COLS)
        gaze = get_cols(slices, GAZE_COLS)
        pose = get_cols(slices, POSE_COLS)
        video_ids = get_fixed_col(slices, "video_id")

        x = {"au": au,
             "gaze": gaze,
             "pose": pose
             }
        x = self.normalize(x, video_ids)

        y = get_fixed_col(slices, "emotion_1_id")

        data = {"x": x,
                "y": y
                }

        with open(os.path.join(ROOT_DIR, "files/out/data.pickle"), "wb") as output_file:
            pickle.dump(data, output_file)

    def normalize(self, x, video_ids):
        for key, values in x.items():
            x[key] = normalize_by_video_id(values, video_ids)
        return x

    def interpolate(self, slices):
        interpolator = Interpolator(self.X_COLS)
        return interpolator.remove_interpolate(slices)


def normalize_by_video_id(slices, video_ids):
    for video_id in np.unique(video_ids):
        boolean_indices = (video_ids == video_id)
        indices = np.where(boolean_indices)[0]

        # get x corresponding to video id indices with boolean indices
        x_video_id = list(compress(slices, boolean_indices))
        if not x_video_id:
            continue

        x_video_id_stack = np.vstack(x_video_id)

        scaler = StandardScaler()
        # fit on all videos corresponding to one video id
        scaler.fit(x_video_id_stack)

        for idx in indices:
            # transform every video in slices
            slices[idx] = scaler.transform(slices[idx])

    return slices


def main():

    d = DatasetCreator()
    d.create()


if __name__ == "__main__":
    main()