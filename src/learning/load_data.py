import os
from dotenv import load_dotenv
from sklearn.utils import shuffle
import pandas as pd
import sklearn as sk
from datetime import datetime

seed = 27


class DataLoader:

    def __init__(self, filename):
        load_dotenv()
        self.path = filename
        df = self.load()

        print("starting at time: " + str(datetime.now()))
        print("loading file {}".format(filename))
        print("with {} rows and {} columns".format(df.shape[0], df.shape[1]))

        self.X = df.drop(columns=["filename", "video_id", "emotion_1_id", "group"])
        self.y = df.emotion_1_id
        self.groups = df.group
        self.n_groups = len(self.groups.unique())

    def load(self):
        df = pd.read_csv(self.path)
        df = shuffle(df, random_state=seed)
        return df
