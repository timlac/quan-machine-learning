import torch
from torch.utils.data import DataLoader, Dataset, random_split
import os
import h5py
from multiprocessing import cpu_count


from global_config import ROOT_DIR


class TimeSeriesDataset(Dataset):

    def __init__(self):
        path = os.path.join(ROOT_DIR, "files/out/low_level/video_data_low_level_np.hdf5")

        f = h5py.File(name=path, mode='r')
        self.x = f['x']
        self.y = f['y']
        self.n_samples = self.y.shape[0]

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples


def train_test_split(dataset):
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train, test = random_split(dataset, [train_size, test_size])
    return train, test

def main():
    dataset = TimeSeriesDataset()
    train_set, test_set = train_test_split(dataset)

    train_loader = DataLoader(dataset=train_set, batch_size=4, shuffle=True, num_workers=cpu_count())
    test_loader = DataLoader(dataset=test_set, batch_size=4, shuffle=True, num_workers=cpu_count())

    dataiter = iter(train_loader)
    data = dataiter.next()
    features, labels = data
    print(features)
    print(labels)


if __name__ == "__main__":
    main()
