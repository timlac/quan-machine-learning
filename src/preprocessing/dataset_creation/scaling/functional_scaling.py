import os

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from global_config import ROOT_DIR, AUDIO_FUNCTIONALS_EGEMAPS_COLS
from src.analysis.data_exploration import plot_means
from src.preprocessing.dataset_creation.scaling.method import Method


def functional_scale_by(x, identifiers, method):
    for identifier in np.unique(identifiers):
        if method == Method.min_max:
            scaler = MinMaxScaler()
        elif method == Method.standard:
            scaler = StandardScaler()
        else:
            raise RuntimeError("Something went wrong, no scaling method chosen")

        rows = np.where(identifiers == identifier)
        x[rows] = scaler.fit_transform(x[rows])
    return x


def main():
    path = os.path.join(ROOT_DIR, "files/out/opensmile_query_13_videos.csv")
    df = pd.read_csv(path)

    x = df[AUDIO_FUNCTIONALS_EGEMAPS_COLS].values
    y = df["emotion_1_id"].values
    video_ids = df["video_id"].values
    intensity_levels = df["intensity_level"].values


    plot_means(x, y, AUDIO_FUNCTIONALS_EGEMAPS_COLS[:5])

    x = functional_scale_by(x, intensity_levels, "standard")
    plot_means(x, y, AUDIO_FUNCTIONALS_EGEMAPS_COLS[:5])


if __name__ == "__main__":
    main()
