import os

import numpy as np
from src.preprocessing.dataset_creation.create_video_functionals import create_functionals
from src.preprocessing.dataset_creation.group_creation import create_groups
from global_config import ROOT_DIR, AU_INTENSITY_COLS, TARGET_COLUMN
from src.preprocessing.dataset_creation.queries import query_au_cols_with_confidence_filter, \
    query_au_cols_without_confidence_filter, query_au_cols_with_confidence_filter_A220
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas


class CreateFunctionalsDataset:

    def __init__(self, save_as, query=None, df=None):
        self.save_as = save_as
        if query:
            self.query = query
            df, _ = execute_sql_pandas(query)
        if df is None:
            raise RuntimeError("Didn't receive query or dataframe on dataset creation")
        self.df = create_functionals(df)

    def get_groups(self):
        video_ids = self.df.video_id
        unique_video_ids = video_ids.unique()

        groups_dict = create_groups(unique_video_ids)
        groups = video_ids.map(groups_dict)

        return groups

    def get_y(self):
        return self.df[TARGET_COLUMN].values

    def get_x(self):
        df_x = self.df.drop(columns=["filename", "video_id", TARGET_COLUMN])
        return df_x.values

    def get_col_names(self):
        df_x = self.df.drop(columns=["filename", "video_id", TARGET_COLUMN])
        return df_x.columns.values

    def save_ds(self):
        print("saving dataset to {}".format(self.save_as))
        x = self.get_x()
        y = self.get_y()
        groups = self.get_groups()
        col_names = self.get_col_names()

        np.savez(self.save_as, x=x, y=y, groups=groups, col_names=col_names)


def main():
    out = os.path.join(ROOT_DIR, "files/out/functionals/video_data_functionals_A220.npz")
    cfs = CreateFunctionalsDataset(out, query=query_au_cols_with_confidence_filter_A220)
    cfs.save_ds()


if __name__ == "__main__":
    main()

