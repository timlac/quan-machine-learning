import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset, random_split
import os
from multiprocessing import cpu_count

import h5py
from src.analysis.data_loading.time_series_dataset import TimeSeriesDataset, train_test_split
from multiprocessing import cpu_count


class LSTMClassifier(nn.Module):
    """Very simple implementation of LSTM-based time-series classifier."""

    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.layer_dim = layer_dim
        self.rnn = nn.LSTM(input_dim, hidden_dim, layer_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax()

    def forward(self, x):
        h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim)
        c0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim)

        out, (hn, cn) = self.rnn(x, (h0, c0))

        out = self.fc(out[:, -1, :])

        # out = self.sigmoid(out)

        out = self.softmax(out)

        return out


dataset = TimeSeriesDataset()
train_set, test_set = train_test_split(dataset)

train_loader = DataLoader(dataset=train_set, batch_size=1, shuffle=True, num_workers=cpu_count())
test_loader = DataLoader(dataset=test_set, batch_size=1, shuffle=True, num_workers=cpu_count())

input_dim = 17
hidden_dim = 256
layer_dim = 3
output_dim = 44

lr = 0.0005
n_epochs = 1000
iterations_per_epoch = len(train_loader)
best_acc = 0

model = LSTMClassifier(input_dim, hidden_dim, layer_dim, output_dim)
print(model)

criterion = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=lr)

print('Start model training')

for i, (x_batch, y_batch) in enumerate(train_loader):
    model.train()

    opt.zero_grad()

    out = model(x_batch)

    print(out)

    print(torch.sum(out))

    loss = criterion(out, y_batch)
    loss.backward()
    opt.step()

    print(loss.item())

# for epoch in range(1, n_epochs + 1):
#
#     for i, (x_batch, y_batch) in enumerate(train_loader):
#         model.train()
#
#         opt.zero_grad()
#
#         out = model(x_batch)
#
#         print(out)
#
#         loss = criterion(out, y_batch)
#         loss.backward()
#         opt.step()
#
#         print(loss.item())