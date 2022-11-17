import os

from src.utils.helpers import list2string
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS, AUDIO_FUNCTIONALS_EGEMAPS_COLS


def openface_query(x_cols):
    query = """SELECT filename,
                    video_id,
                    intensity_level,
                    emotion_1_id,
                    success,
                    confidence,
                    `{X_COLS}`
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
    df.to_csv(os.path.join(ROOT_DIR, "files/out/openface_query.csv"), index=False)


def opensmile_query(x_cols):

    # print(x_cols)

    # print(list2string(x_cols))

    query = """SELECT filename,
                        video_id,
                        intensity_level,
                        emotion_1_id,
                        `{X_COLS}`
                        FROM opensmile_functionals
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

    # print(query)

    df, _ = execute_sql_pandas(query)

    df.to_csv(os.path.join(ROOT_DIR, "files/out/opensmile_functionals_query.csv"), index=False)


def main():
    # x_cols = [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS]
    # openface_query(x_cols)

    x_cols = AUDIO_FUNCTIONALS_EGEMAPS_COLS
    # opensmile_query(x_cols)


if __name__ == "__main__":
    main()
