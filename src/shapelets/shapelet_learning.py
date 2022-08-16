import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.decomposition import PCA


from tslearn.shapelets import LearningShapelets
from keras.optimizers import adam_v2
from dotenv import load_dotenv

from src.global_config import AU_INTENSITY_COLS


df = pd.read_csv('~/work/su-thesis-project/emotional-recognition/files/tests/out/video/video_data_time_series_ang_sad.csv')

X_list = []
y_list = []
for _, group in df.groupby('filename'):
    x_arr = np.array(group[AU_INTENSITY_COLS[10:11]].values)
    if group[['emotion_1_id']].values[0] == 12:
        y_list.append(1)
    else:
        y_list.append(0)
    X_list.append(x_arr)

length = max(map(len, X_list))

padded_X = []
for xi in X_list:
    pad = np.zeros((length-len(xi), xi.shape[1]))
    xi = np.concatenate((xi, pad)).T
    padded_X.append(xi)

X = np.asarray(padded_X)

X = X.reshape((486, 1549, 1))
#X = X[:, :50, :]

y = np.array(y_list)
#y = y[:]

# We will extract 2 shapelets and align them with the time series
shapelet_sizes = {50: 10}

# Define the model and fit it using the training data
clf = LearningShapelets(n_shapelets_per_size=shapelet_sizes,
                        weight_regularizer=0.0001,
                        max_iter=2,
                        verbose=100,
                        scale=False,
                        random_state=42)
clf.fit(X, y)

# We will plot our distances in a 2D space
distances = clf.transform(X)
weights, biases = clf.get_weights('classification')

print(distances)

pca = PCA(n_components=2)
pca.fit(distances)
pc_distances = pca.transform(distances)


colors = ['red', 'blue']
plt.scatter(pc_distances[:, 0], pc_distances[:, 1], c=y, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

out = clf.predict(X)
correct = (out == y).sum()
total = len(y)
acc = correct/total

print("accuracy: " + str(acc))


# dist_df = pd.DataFrame(distances)
# dist_df.to_csv("distances.csv", index=False)
#
# y_df = pd.DataFrame(y)
# y_df.to_csv("labels.csv")