from enum import Enum
from itertools import compress

import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from global_config import ROOT_DIR, AU_INTENSITY_COLS, POSE_COLS
from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col

from src.analysis.data_exploration import plot_time_series_means, plot_time_series_means_subplots


class Method(str, Enum):
    min_max = "min_max"
    standard = "standard"


class Scaler:

    def __init__(self, slices, method):
        self.slices = slices

        if method == Method.min_max or method == Method.standard:
            self.method = method
        else:
            raise ValueError("invalid scaling method: {}".format(method))

    def scale_by_video_id(self, video_ids):
        for slice_chunk, indices in chunk_data(video_ids, self.slices):
            self.scale(slice_chunk, indices)

    def scale_by_video_id_and_intensity(self, video_ids, intensity_levels):
        for slice_chunk_1, _ in chunk_data(video_ids, self.slices):
            for slice_chunk_2, indices in chunk_data(intensity_levels, slice_chunk_1):
                self.scale(slice_chunk_2, indices)

    def scale_by_intensity(self, intensity_levels):
        for slice_chunk, indices in chunk_data(intensity_levels, self.slices):
            self.scale(slice_chunk, indices)

    def scale(self, slice_chunk, indices):
        slices_as_array = np.vstack(slice_chunk)

        if self.method == Method.standard:
            scaler = StandardScaler()
        elif self.method == Method.min_max:
            scaler = MinMaxScaler()
        else:
            raise RuntimeError("Something went wrong, no scaling method chosen")

        # fit on all videos in chunk
        scaler.fit(slices_as_array)

        for idx in indices:
            # transform every video in chunk indices
            self.slices[idx] = scaler.transform(self.slices[idx])


def chunk_data(chunk_identifiers, slices):
    for chunk_identifier in np.unique(chunk_identifiers):
        boolean_indices = (chunk_identifiers == chunk_identifier)
        indices = np.where(boolean_indices)[0]

        # get slices corresponding to chunk indices
        slice_chunk = list(compress(slices, boolean_indices))

        yield slice_chunk, indices


def main():
    df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/query.csv"))

    slices = slice_by(df, "filename")

    au = get_cols(slices, AU_INTENSITY_COLS)

    video_ids = get_fixed_col(slices, "video_id")

    for i in np.unique(video_ids):
        print(i)

    intensity_level = get_fixed_col(slices, "intensity_level")
    y = get_fixed_col(slices, "emotion_1_id")

    scaler = Scaler(au, "standard")
    # scaler.scale_by_intensity(intensity_level)
    scaler.scale_by_video_id_and_intensity(video_ids, intensity_level)

    au_scaled = scaler.slices

    au = get_cols(slices, AU_INTENSITY_COLS)

    plot_time_series_means_subplots(au, au_scaled, y, AU_INTENSITY_COLS)


if __name__ == "__main__":
    main()
