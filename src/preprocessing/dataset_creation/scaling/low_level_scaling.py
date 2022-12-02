from itertools import compress

import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from global_config import ROOT_DIR, AU_INTENSITY_COLS
from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col

from src.preprocessing.dataset_creation.scaling.method import Method


def low_level_scale_by(slices, by, method):
    for slice_chunk, indices in chunk_data(by, slices):
        slices_as_array = np.vstack(slice_chunk)

        if method == Method.standard:
            scaler = StandardScaler()
        elif method == Method.min_max:
            scaler = MinMaxScaler()
        else:
            raise RuntimeError("Something went wrong, no scaling method chosen")

        # fit on all videos in chunk
        scaler.fit(slices_as_array)

        for idx in indices:
            # transform every video in chunk indices
            slices[idx] = scaler.transform(slices[idx])
    return slices


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

    au_scaled = low_level_scale_by(au, video_ids, method="min_max")

    # plot_time_series_means_subplots(au, au_scaled, y, AU_INTENSITY_COLS)


if __name__ == "__main__":
    main()
