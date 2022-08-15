import torch as torch
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from torch.nn.utils.rnn import pad_sequence

from src.global_config import AU_INTENSITY_COLS


class LogisticRegression(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)

    def forward(self, x):
        output = torch.sigmoid(self.linear(x))
        return output


class Trainer:
    epochs = 20000
    learning_rate = 0.01

    def __init__(self, x, y, n_features, n_classes):
        if not torch.is_tensor(x):
            x = torch.tensor(x)
        if not torch.is_tensor(y):
            y = torch.tensor(y)

        self.model = LogisticRegression(n_features, n_classes)
        self.criterion = torch.nn.BCELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y)

    def train(self):
        for epoch in range(self.epochs):
            self.model.train()
            self.optimizer.zero_grad()  # Setting our stored gradients equal to zero
            output = self.model(self.x_train.float())

            loss = self.criterion(torch.squeeze(output).float(), self.y_train.float())
            loss.backward()  # Computes the gradient of the given tensor w.r.t. graph leaves

            self.optimizer.step()  # Updates weights and biases with the optimizer (SGD)

            if epoch % 100 == 0:
                self.model.eval()
                train_acc = self.get_accuracy(self.x_train, self.y_train)
                valid_acc = self.get_accuracy(self.x_test, self.y_test)

                print("Loss: {}".format(loss.item()))
                #print("Train Accuracy: {}".format(train_acc))
                #print("Validation Accuracy: {}".format(valid_acc))

    def get_accuracy(self, x, y):
        correct, total = 0, 0
        out = self.model(x.float())
        predictions = np.round(out.detach()).squeeze()
        total += y.size(0)
        correct = (predictions == y).sum()
        acc = correct / total
        return acc


def main():
    df = pd.read_csv(
        '~/work/su-thesis-project/emotional-recognition/files/tests/out/video/video_data_time_series_ang_sad.csv')

    x = []
    y = []
    for _, group in df.groupby('filename'):
        x_arr = torch.tensor(group[AU_INTENSITY_COLS].values)
        if group[['emotion_1_id']].values[0] == 12:
            y.append(1)
        else:
            y.append(0)
        x.append(x_arr)

    x_pad = pad_sequence(x, batch_first=True)
    y_tensor = torch.tensor(y)
    x_tensor = torch.reshape(x_pad, (x_pad.shape[0], x_pad.shape[1] * 17))

    trainer = Trainer(x_tensor, y_tensor, x_pad.shape[1] * 17, 1)
    trainer.train()


#if __name__ == "__main__":
 #   main()

