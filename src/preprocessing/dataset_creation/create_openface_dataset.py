import os

import numpy as np
from itertools import compress
from sklearn.preprocessing import StandardScaler
import pickle

from src.preprocessing.dataset_creation.scaling import Scaler
from src.utils.helpers import list2string
from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS
from src.preprocessing.dataset_creation.interpolation import Interpolator

from src.preprocessing.dataset_creation.torch_pad import get_padded_time_series_with_torch


def normalize(x, video_ids):
    for group, slices in x.items():
        scaler = Scaler(slices)
        scaler.scale_by_video_id(video_ids)
        x[group] = scaler.slices
    return x


class DatasetCreator:

    X_COLS = [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS]

    # padding value for time series datasets
    # variable length time series requires padding to create an array with same length rows
    PADDING_VALUE = -1000

    # AND VIDEO_ID NOT IN('A050121-R', 'A21', 'A34')

    query = """SELECT filename,
                    video_id,
                    intensity_level,
                    emotion_1_id,
                    success,
                    confidence,
                    `{X_COLS}`
                    FROM openface
                    WHERE mix = 0
                    AND video_id IN ('A101',
                                        'A102',
                                        'A103',
                                        'A18',
                                        'A200',
                                        'A201',
                                        'A205',
                                        'A207',
                                        'A218',
                                        'A220',
                                        'A221',
                                        'A223',                                        
                                        'A227')
                    ;""".format(X_COLS=list2string(X_COLS))

    def __init__(self,
                 aggregate=True):

        # aggregate (create functionals) or not (only applicable for openface features
        self.aggregate = aggregate

    def create(self):
        df, _ = execute_sql_pandas(self.query)
        df.to_csv(os.path.join(ROOT_DIR, "files/out/query.csv"), index=False)

        # df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/query.csv"))

        # slices = slice_by(df, "filename")
        # slices = self.interpolate(slices)
        #
        # au = get_cols(slices, AU_INTENSITY_COLS)
        # gaze = get_cols(slices, GAZE_COLS)
        # pose = get_cols(slices, POSE_COLS)
        # video_ids = get_fixed_col(slices, "video_id")
        # intensity_level = get_fixed_col(slices, "intensity_level")
        #
        # x = {"au": au,
        #      "gaze": gaze,
        #      "pose": pose
        #      }
        #
        # x = self.normalize(x, video_ids)
        #
        # y = get_fixed_col(slices, "emotion_1_id")
        #
        # self.save_as_pickle(x, y, video_ids, intensity_level)
        # self.save_as_numpy_ts(x, y)

    def save_as_pickle(self, x, y, video_ids, intensity_level):
        data = {"x": x,
                "y": y,
                "video_id": video_ids,
                "intensity_level": intensity_level
                }

        with open(os.path.join(ROOT_DIR, "files/out/intensity_23_mode_p_minmax_normalized.pickle"), "wb") as output_file:
            pickle.dump(data, output_file)

    def save_as_numpy_ts(self, x, y):
        x = self.pad_lists(x)

        for i in x:
            print(i.shape)
        np.savez_compressed(os.path.join(ROOT_DIR, "files/out/intensity_23_.pickle"), au=x["au"], gaze=x["gaze"], pose=x["pose"], y=y)

    def pad_lists(self, x):
        for key, value in x.items():
            x[key] = get_padded_time_series_with_torch(value)
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