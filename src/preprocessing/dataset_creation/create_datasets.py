import os

import numpy as np
import pandas as pd
from src.preprocessing.dataset_creation.time_series_handling import pad_list_of_series, time_series_to_list
from src.preprocessing.dataset_creation.create_video_functionals import create_functionals
from src.preprocessing.dataset_creation.group_creation import create_video_id_groups
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, TARGET_COLUMN
from src.preprocessing.dataset_creation.queries import query_au_cols_with_confidence_filter, \
    query_au_cols_without_confidence_filter, query_au_cols_with_confidence_filter_A220


def create_time_series_ds(df, save_as):
    x, y = time_series_to_list(df, "filename", AU_INTENSITY_COLS, TARGET_COLUMN)
    x = pad_list_of_series(x)
    print("saving dataset to {}".format(save_as))
    np.savez(save_as, x=x, y=y)


def query_db(query):
    print("Executing query".format(query))
    df, read_duration = execute_sql_pandas(query)
    print("Read duration: {}".format(read_duration))
    return df


# def create_functionals_ds(query, save_as):
#     df = query_db(query)
#     groups_dict = create_groups(df.video_id.unique())
#     groups = df.video_id.map(groups_dict)
#     y = df[TARGET_COLUMN].values
#     df = df.drop(columns=["filename", "video_id", TARGET_COLUMN])
#     x = df.values
#     col_names = df.columns.values
#     print("saving dataset to {}".format(save_as))
#     np.savez(save_as, x=x, y=y, groups=groups, col_names=col_names)




#
# query = query_au_cols_with_confidence_filter_A220
# out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data_functionals.npz")
#
# load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data.csv")
# df = pd.read_csv(load, nrows=10000)
#
# cfs = CreateFunctionalsDataset(out, df=df)


#
# def main():
#     query = query_au_cols_with_confidence_filter_A220
#     out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data_functionals.npz")
#     create_functionals_ds(query, out)

    # query = query_au_cols_without_confidence_filter
    # df = query_db(query)
    # out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data_with_unsuccessful.csv")
    # df.to_csv(out, index=False)

    # query = query_au_cols_with_confidence_filter_A220
    # df = query_db(query)
    # out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data_functionals_A220.npz")
    # create_functionals_ds(df, out)

    # load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data.csv")
    # df = pd.read_csv(load, nrows=10000)
    # out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data_functionals.npz")
    # create_functionals_ds(df, out)


    # out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data.csv")
    # df.to_csv(out, index=False)

    # load = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/video_data.csv")
    # df = pd.read_csv(load, nrows=10000)
    #
    # out = os.path.join(ROOT_DIR, "files/tests/preprocessing/dataset_creation/padded_time_series.npz")
    # create_time_series_ds(df, out)


# if __name__ == "__main__":
#     main()
