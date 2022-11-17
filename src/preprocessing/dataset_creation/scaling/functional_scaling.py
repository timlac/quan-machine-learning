import os

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from global_config import ROOT_DIR, AUDIO_FUNCTIONALS_EGEMAPS_COLS
from src.analysis.data_exploration import plot_means
from src.preprocessing.dataset_creation.scaling.method import Method


def scale_by_video_id(x, video_ids, method):
    for video_id in np.unique(video_ids):
        if method == Method.min_max:
            scaler = MinMaxScaler()
        elif method == Method.standard:
            scaler = StandardScaler()
        else:
            raise RuntimeError("Something went wrong, no scaling method chosen")

        rows = np.where(video_ids == video_id)
        x[rows] = scaler.fit_transform(x[rows])
    return x


def main():
    path = os.path.join(ROOT_DIR, "files/out/opensmile_query_13_videos.csv")
    df = pd.read_csv(path)

    x = df[AUDIO_FUNCTIONALS_EGEMAPS_COLS].values
    y = df["emotion_1_id"].values
    video_ids = df["video_id"].values

    plot_means(x, y, AUDIO_FUNCTIONALS_EGEMAPS_COLS[:5])

    x = scale_by_video_id(x, video_ids, "standard")
    plot_means(x, y, AUDIO_FUNCTIONALS_EGEMAPS_COLS[:5])


if __name__ == "__main__":
    main()
    