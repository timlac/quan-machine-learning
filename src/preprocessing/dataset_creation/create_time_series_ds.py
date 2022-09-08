import pandas as pd
import torch

from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from src.preprocessing.dataset_creation.time_series_handling import pad_list_of_series, time_series_to_list
from global_config import ROOT_DIR, AU_INTENSITY_COLS, TARGET_COLUMN
from torch.nn.utils.rnn import pad_sequence
import numpy as np
import os
import h5py
from missing_time_series_values_handling import MissingTimeSeriesValuesHandler

from src.preprocessing.dataset_creation.queries import query_au_cols_without_confidence_filter
from enum import Enum


class CreateTimeSeriesDataset:

    SLICE_BY = "filename"
    VIDEO_ID = "video_id"

    def __init__(self, save_as, query=None, df=None):
        self.save_as = save_as

        if query:
            self.query = query
            df, _ = execute_sql_pandas(query)
        else:
            self.query = None
        if df is None:
            raise RuntimeError("Didn't receive query or dataframe on dataset creation")

        missing_handler = MissingTimeSeriesValuesHandler()
        self.df = missing_handler.remove_and_interpolate(df)
        self.x, self.y = time_series_to_list(df, self.SLICE_BY, AU_INTENSITY_COLS, TARGET_COLUMN)

    def get_x(self):
        x = pad_sequence(self.x, batch_first=True)
        return np.array(x)

    def get_y(self):
        return np.array(self.y)

    def save(self):
        print("saving data to {}".format(self.save_as))

        f = h5py.File(name=self.save_as, mode='w')

        # save data
        f['x'] = self.get_x()
        f['y'] = self.get_y()

        if self.query:
            f.attrs['query'] = self.query
        f.close()


def test():
    inp = "/home/tim/work/su-thesis-project/emotional-recognition/files/out/au_cols_without_confidence_filter.csv"
    out = os.path.join(ROOT_DIR, "files/out/low_level/video_data_low_level_np.hdf5")
    df = pd.read_csv(inp)
    creator = CreateTimeSeriesDataset(out,
                                      df=df)
    creator.save()


def main():
    out = os.path.join(ROOT_DIR, "files/out/low_level/video_data_low_level.hdf5")
    creator = CreateTimeSeriesDataset(out, query=query_au_cols_without_confidence_filter)
    creator.save()


if __name__ == "__main__":
    test()