from datetime import datetime
import h5py
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

from global_config import ROOT_DIR
import os

seed = 27


def load_h5(path):
    f = h5py.File(path, 'r')
    print("attributes")
    for k in f.attrs.keys():
        print(f"{k} : {f.attrs[k]}")
    return f


def scale(x):
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    return x


class DataLoader:

    def __init__(self, path):
        file = load_h5(path)
        x = file['x']
        self.x = scale(x)

        self.y = np.array(file['y'])
        self.groups = np.array(file['groups'])
        self.n_groups = len(np.unique(self.groups))

        # shuffle x, y and groups together
        self.x, self.y, self.groups = shuffle(self.x, self.y, self.groups)

        print("starting at time: " + str(datetime.now()))
        print("loading file {}".format(path))
        print("with {} rows and {} columns".format(self.x.shape[0], self.x.shape[1]))


def main():
    path = os.path.join(ROOT_DIR, "files/out/functionals/video_data_functionals_A220.hdf5")

    data = DataLoader(path)

    print(data.x)
    print(data.y)
    print(data.groups)


if __name__ == "__main__":
    main()
