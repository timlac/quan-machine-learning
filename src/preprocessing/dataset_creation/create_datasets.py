import os
import numpy as np

from src.preprocessing.dataset_creation.helpers import get_padded_time_series, get_fixed_col, \
    slice_by
from src.preprocessing.dataset_creation.aggregation import get_aggregate_measures
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS
from src.preprocessing.sql_handling.queries import query_au_cols, query_gaze_cols
from src.preprocessing.dataset_creation.interpolation import Interpolator


class DatasetCreator:
    # every time series in the dataset is identified by a unique filename
    TIMESERIES_IDENTIFIER = "filename"

    # padding value for time series datasets
    # variable length time series requires padding to create an array with same length rows
    PADDING_VALUE = -1000

    INTENSITY_COL = "intensity_level"
    MODE_COL = "mode"

    def __init__(self,
                 query,
                 X_COLS,
                 Y_COL,
                 interpolate=True,
                 aggregate=True):

        # query for the database
        self.query = query
        # name of columns
        self.X_COLS = X_COLS
        self.Y_COL = Y_COL

        # interpolate or not (only applicable for openface features)
        self.interpolate = interpolate
        # aggregate (create functionals) or not (only applicable for openface features
        self.aggregate = aggregate

    def create(self, save_as):
        df, _ = execute_sql_pandas(self.query)

        df.to_csv(os.path.join(ROOT_DIR, "files/out/audio_cols.csv"), index=False)

        # df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/au_cols_without_confidence_filter.csv"))

        slices = slice_by(df, self.TIMESERIES_IDENTIFIER)

        if self.interpolate:
            interpolator = Interpolator(self.X_COLS)
            slices = interpolator.remove_interpolate(slices)

        if self.aggregate:
            x = get_aggregate_measures(slices, self.X_COLS)
        else:
            x = get_padded_time_series(slices, self.X_COLS, self.PADDING_VALUE)

        y = get_fixed_col(slices, self.Y_COL)
        intensity_level = get_fixed_col(slices, self.INTENSITY_COL)
        mode = get_fixed_col(slices, self.MODE_COL)

        print("x shape: ", x.shape)
        print("y shape: ", y.shape)
        print("intensity_level shape: ", intensity_level.shape)
        print("mode shape: ", mode.shape)

        np.savez_compressed(save_as, x=x, y=y, intensity_level=intensity_level, mode=mode)


def main():
    # Pose
    # TODO: Try to analyze how pose is different between different emotions?
    # TODO: Is there any particular feature that stands out?
    # pose_dataset_creator = DatasetCreator(query=query_pose_cols,
    #                                       X_COLS=POSE_COLS,
    #                                       Y_COL="emotion_1_id",
    #                                       interpolate=True,
    #                                       aggregate=True,
    #                                       )
    # pose_save_path = os.path.join(ROOT_DIR, "files/out/functionals/video_pose_functionals.npz")
    # pose_dataset_creator.create(pose_save_path)

    # audio time series
    # audio_time_series_creator = DatasetCreator(query=query_audio_cols,
    #                                            X_COLS=AUDIO_LLD_COLS,
    #                                            interpolate=False,
    #                                            aggregate=False)
    # audio_time_series_save_path = os.path.join(ROOT_DIR, "files/out/low_level/audio_time_series_intensity_4.npz")
    # audio_time_series_creator.create(audio_time_series_save_path)

    # action unit time series
    # video_time_series_creator = DatasetCreator(query="",
    #                                            X_COLS=AU_INTENSITY_COLS,
    #                                            interpolate=False,
    #                                            aggregate=False)
    # video_time_series_save_path = os.path.join(ROOT_DIR, "files/out/low_level/video_time_series.npz")
    # video_time_series_creator.create(video_time_series_save_path)

    # action unit functionals
    # au_functionals_creator = DatasetCreator(query=query_au_cols,
    #                                         X_COLS=AU_INTENSITY_COLS,
    #                                         Y_COL="emotion_1_id",
    #                                         interpolate=True,
    #                                         aggregate=True)
    # au_save_path = os.path.join(ROOT_DIR, "files/out/functionals/au_functionals_only_means.npz")
    # au_functionals_creator.create(au_save_path)

    # gaze functionals
    gaze_functionals_creator = DatasetCreator(query=query_gaze_cols,
                                              X_COLS=GAZE_COLS,
                                              Y_COL="emotion_1_id",
                                              interpolate=True,
                                              aggregate=True)
    gaze_save_path = os.path.join(ROOT_DIR, "files/out/functionals/gaze_functionals.npz")
    gaze_functionals_creator.create(gaze_save_path)

    # gemep time series
    # audio_time_series_creator = DatasetCreator(query=query_audio_cols_gemep,
    #                                            X_COLS=COMPARE_AUDIO_LLD_COLS,
    #                                            Y_COL="emotion_id",
    #                                            interpolate=False,
    #                                            aggregate=False)
    # audio_time_series_save_path = os.path.join(ROOT_DIR, "files/out/low_level/gemep_compare_audio_time_series.npz")
    # audio_time_series_creator.create(audio_time_series_save_path)


if __name__ == "__main__":
    main()
