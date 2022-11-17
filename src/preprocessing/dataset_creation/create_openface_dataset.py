import os

import numpy as np
from itertools import compress
from sklearn.preprocessing import StandardScaler
import pickle

from src.preprocessing.dataset_creation.scaling import Scaler
from src.utils.helpers import list2string
from src.preprocessing.dataset_creation.helpers import slice_by, get_cols, get_fixed_col
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS
from src.preprocessing.dataset_creation.interpolation import Interpolator

from src.preprocessing.dataset_creation.torch_pad import get_padded_time_series_with_torch


def create_csv_from_query(x_cols):

    query = """SELECT filename,
                    video_id,
                    intensity_level,
                    emotion_1_id,
                    success,
                    confidence,
                    `{x_cols}`
                    FROM openface
                    WHERE mix = 0
                    AND video_id IN ('A101',
                                        'A102',
                                        'A103',
                                        'A18',
                                        'A200',
                                        'A201',
                                        'A205',
                                        'A207',
                                        'A218',
                                        'A220',
                                        'A221',
                                        'A223',                                        
                                        'A227')
                    ;""".format(X_COLS=list2string(x_cols))

    df, _ = execute_sql_pandas(query)
    df.to_csv(os.path.join(ROOT_DIR, "files/out/query.csv"), index=False)


def main():
    x_cols = [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS]
    create_csv_from_query(x_cols)


if __name__ == "__main__":
    main()
