import os
import matplotlib.pyplot as plt

import numpy as np
import numpy.ma as ma
import pandas as pd

from scipy.stats.mstats import kurtosis


from global_config import ROOT_DIR, emotion_id_to_emotion, GAZE_COLS, basic_emotion_ids, AU_INTENSITY_COLS, \
    au_intensity_name_to_desc
from src.preprocessing.dataset_creation.helpers import get_padded_time_series_with_numpy, slice_by, get_cols, \
    get_fixed_col


def plot_stds(x, y, cols):
    x = ma.masked_where(x == -1000, x)

    for idx, col in enumerate(cols):
        means = {}
        stds = {}
        for emotion_id, emotion in emotion_id_to_emotion.items():

            emotion_indices = np.where(y == emotion_id)[0]
            x_emotion = x[emotion_indices]
            x_emotion_col = x_emotion[:, :, idx]

            std_arr = np.std(x_emotion_col, axis=1)

            means[emotion] = np.mean(std_arr)
            stds[emotion] = np.std(std_arr)

        plt.figure(figsize=(15, 10))
        plt.errorbar(means.keys(), means.values(), yerr=list(stds.values()),
                     fmt='o', ecolor="black", capsize=2, elinewidth=1)
        plt.title(col)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


def plot_time_series_means(slices, y, cols):
    padding_value = -1000
    x = get_padded_time_series_with_numpy(slices, padding_value)
    x = ma.masked_where(x == padding_value, x)

    for idx, col in enumerate(cols):
        plt.figure(figsize=(15, 10))

        for emotion_id, emotion in emotion_id_to_emotion.items():
            if emotion_id in basic_emotion_ids:

                emotion_indices = np.where(y == emotion_id)[0]
                x_emotion = x[emotion_indices]

                x_emotion_col = x_emotion[:, :, idx]

                means = np.mean(x_emotion_col, axis=0)
                stds = np.std(x_emotion_col, axis=0)

                plt.plot(range(len(means)), means, label=emotion)
                plt.fill_between(range(len(means)), means - stds, means + stds, alpha=0.3)

        plt.xlim(0, 350)
        plt.title(au_intensity_name_to_desc[col])
        plt.legend()
        plt.show()


def mask_and_pad(slices):
    padding_value = -1000
    x = get_padded_time_series_with_numpy(slices, padding_value)
    x = ma.masked_where(x == padding_value, x)
    return x


def get_means_and_stds(x, emotion_indices, col_idx):
    x_emotion = x[emotion_indices]
    x_emotion_col = x_emotion[:, :, col_idx]

    means = np.mean(x_emotion_col, axis=0)
    stds = np.std(x_emotion_col, axis=0)

    return means, stds


def plot_time_series_means_subplots(slices_1, slices_2, y, cols):
    x1 = mask_and_pad(slices_1)
    x2 = mask_and_pad(slices_2)

    for idx, col in enumerate(cols):
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 10))
        axes[0].set_title("Pre")
        axes[1].set_title("Post")
        for emotion_id, emotion in emotion_id_to_emotion.items():
            if emotion_id in basic_emotion_ids:

                emotion_indices = np.where(y == emotion_id)[0]

                means_1, stds_1 = get_means_and_stds(x1, emotion_indices, idx)

                means_2, stds_2 = get_means_and_stds(x2, emotion_indices, idx)

                axes[0].plot(range(len(means_1)), means_1, label=emotion)
                axes[0].fill_between(range(len(means_1)), means_1 - stds_1, means_1 + stds_1, alpha=0.3)

                axes[1].plot(range(len(means_2)), means_2, label=emotion)
                axes[1].fill_between(range(len(means_2)), means_2 - stds_2, means_2 + stds_2, alpha=0.3)

        axes[0].set_xlim(0, 350)
        axes[1].set_xlim(0, 350)

        handles, labels = axes[1].get_legend_handles_labels()
        fig.legend(handles, labels)
        fig.suptitle(au_intensity_name_to_desc[col])
        plt.show()


def plot_means(x, y, cols):
    for idx, col in enumerate(cols):
        means = {}
        stds = {}

        for emotion_id, emotion in emotion_id_to_emotion.items():

            emotion_indices = np.where(y == emotion_id)[0]
            x_emotion = x[emotion_indices]
            x_emotion_col = x_emotion[:, idx]
            means[emotion] = np.mean(x_emotion_col)
            stds[emotion] = np.std(x_emotion_col)

        plt.figure(figsize=(15, 10))
        plt.errorbar(means.keys(), means.values(), yerr=list(stds.values()),
                     fmt='o', ecolor="black", capsize=2, elinewidth=1)
        plt.title(col)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


def get_mean_length(slices):
    lens = []
    for sli in slices:
        lens.append(sli.shape[0])
    lens = np.array(lens)
    m = np.mean(lens)
    s = np.std(lens)
    max_len = np.max(lens)

    print(m)
    print(s)
    print(max_len)


def main():
    df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/query.csv"))

    slices = slice_by(df, "filename")

    cols = AU_INTENSITY_COLS

    au = get_cols(slices, cols)

    y = get_fixed_col(slices, "emotion_1_id")

    plot_time_series_means_subplots(au, au, y, cols)


if __name__ == "__main__":
    main()
