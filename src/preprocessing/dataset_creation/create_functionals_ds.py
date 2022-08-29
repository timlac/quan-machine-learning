import os

import numpy as np
import pandas as pd
import h5py

from constants import CONSTANTS
from src.preprocessing.dataset_creation.create_video_functionals import create_functionals
from src.preprocessing.dataset_creation.group_creation import create_video_id_groups, create_twinned_groups
from global_config import ROOT_DIR, AU_INTENSITY_COLS, TARGET_COLUMN
from src.preprocessing.dataset_creation.queries import query_au_cols_with_confidence_filter, \
    query_au_cols_without_confidence_filter, query_au_cols_with_confidence_filter_A220
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas


class CreateFunctionalsDataset:

    def __init__(self, save_as, group_type, query=None, df=None):
        self.save_as = save_as
        self.group_type = group_type
        if query:
            self.query = query
            df, _ = execute_sql_pandas(query)
        else:
            self.query = None
        if df is None:
            raise RuntimeError("Didn't receive query or dataframe on dataset creation")
        self.df = create_functionals(df)

    def get_groups(self, group_type):
        if group_type == CONSTANTS.TWINNED:
            filenames = self.df.filename
            groups_dict = create_twinned_groups(filenames)
            groups = filenames.map(groups_dict)
        elif group_type == CONSTANTS.VIDEO_ID:
            video_ids = self.df.video_id
            unique_video_ids = video_ids.unique()
            groups_dict = create_video_id_groups(unique_video_ids)
            groups = video_ids.map(groups_dict)
        else:
            raise ValueError("No group type specified")
        return groups

    def get_y(self):
        return self.df[TARGET_COLUMN].values

    def get_x(self):
        df_x = self.df.drop(columns=["filename", "video_id", TARGET_COLUMN])
        return df_x.values

    def get_feature_names(self):
        df_x = self.df.drop(columns=["filename", "video_id", TARGET_COLUMN])
        return df_x.columns.values

    def save_ds(self):
        print("saving dataset to {}".format(self.save_as))

        f = h5py.File(name=self.save_as, mode='w')
        # save data
        f['x'] = self.get_x()
        f['y'] = self.get_y()
        f['groups'] = self.get_groups(group_type=self.group_type)
        f['feature_names'] = self.get_feature_names()

        # save metadata
        f.attrs['group_type'] = self.group_type
        if self.query:
            f.attrs['query'] = self.query
        f.close()


def main():
    # load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data_functionals_A220.npz")
    # df = pd.read_csv(load)

    out = os.path.join(ROOT_DIR, "files/out/functionals/video_data_functionals.hdf5")
    cfs = CreateFunctionalsDataset(out, group_type=CONSTANTS.VIDEO_ID, query=query_au_cols_with_confidence_filter)
    # cfs = CreateFunctionalsDataset(out, group_type=CONSTANTS.TWINNED, df=df)

    cfs.save_ds()


if __name__ == "__main__":
    main()
