from global_config import ROOT_DIR, emotion_id_to_emotion, GAZE_COLS, basic_emotion_ids
import os
import matplotlib.pyplot as plt

import numpy as np
import numpy.ma as ma

from scipy.stats.mstats import kurtosis


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


def plot_time_series_means(x, y, cols):
    x = ma.masked_where(x == -1000, x)

    for idx, col in enumerate(cols):
        plt.figure(figsize=(15, 10))

        for emotion_id, emotion in emotion_id_to_emotion.items():
            emotion_indices = np.where(y == emotion_id)[0]
            x_emotion = x[emotion_indices]

            x_emotion_col = x_emotion[:, :, idx]

            means = np.mean(x_emotion_col, axis=0)

            plt.plot(means, label=emotion)

        # bbox_inches = "tight"
        plt.title(col)
        plt.legend()
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


def main():
    # path = os.path.join(ROOT_DIR, "files/out/functionals/gaze_functionals.npz")
    path = os.path.join(ROOT_DIR, "files/out/low_level/gaze_lld.npz")

    f = np.load(path, 'r')
    x = f['x']
    y = f['y']

    plot_means(x, y, GAZE_COLS)


if __name__ == "__main__":
    main()
