from global_config import ROOT_DIR, emotion_id_to_emotion, GAZE_COLS, basic_emotion_ids
import os
import matplotlib.pyplot as plt

import numpy as np
import numpy.ma as ma

from scipy.stats.mstats import kurtosis



# plt.rcParams["figure.figsize"] = (15, 10)


def plot_stds(cols, x, y):
    x = ma.masked_where(x == -1000, x)

    for idx, col in enumerate(cols):
        means = {}
        stds = {}
        for emotion_id, emotion in emotion_id_to_emotion.items():
            # print(emotion)
            # print(idx)
            emotion_indices = np.where(y == emotion_id)[0]
            x_emotion = x[emotion_indices]
            x_emotion_col = x_emotion[:, :, idx]

            # std_arr = np.std(x_emotion_col, axis=1)

            std_arr = kurtosis(x_emotion_col, axis=1)
            

            # mean = np.mean(std_arr)
            # std = np.std(std_arr)
            #
            # print(mean)
            # print(std)

            means[emotion] = np.mean(std_arr)
            stds[emotion] = np.std(std_arr)

        plt.figure(figsize=(15, 10))
        plt.errorbar(means.keys(), means.values(), yerr=list(stds.values()),
                     fmt='o', ecolor="black", capsize=2, elinewidth=1)
        plt.title(col)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


# def plot_time_series(cols, x, y):



def plot_time_series_means(cols, x, y):
    x = ma.masked_where(x == -1000, x)

    plt.figure(figsize=(15, 10))

    for idx, col in enumerate(cols):
        for emotion_id, emotion in emotion_id_to_emotion.items():
            emotion_indices = np.where(y == emotion_id)[0]
            x_emotion = x[emotion_indices]

            x_emotion_col = x_emotion[:, :, idx]

            means = np.mean(x_emotion_col, axis=0)

            plt.plot(means, label=emotion)

        plt.title(col)
        plt.legend()
        plt.show()


def plot_means(cols, x, y):
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

    plot_stds(GAZE_COLS, x, y)


if __name__ == "__main__":
    main()
