import os

from src.utils.helpers import list2string
from src.preprocessing.sql_handling.execute_sql import execute_sql_pandas
from global_config import ROOT_DIR, AU_INTENSITY_COLS, GAZE_COLS, POSE_COLS, AUDIO_FUNCTIONALS_EGEMAPS_COLS, \
    AUDIO_LLD_COLS


def openface_query(x_cols):
    query = """SELECT filename,
                    video_id,
                    filename,
                    intensity_level,
                    emotion_1_id,
                    success,
                    confidence,
                    `{X_COLS}`
                    FROM openface
                    WHERE mix = 0
                    AND video_id IN ('A223',
                                        'A220',
                                        'A91')
                    AND mode = 'v'
                    ;""".format(X_COLS=list2string(x_cols))

    df, _ = execute_sql_pandas(query)
    df.to_csv(os.path.join(ROOT_DIR, "files/out/openface_query.csv"), index=False)


def opensmile_functionals_query(x_cols):

    # print(x_cols)

    # print(list2string(x_cols))

    query = """SELECT filename,
                        video_id,
                        filename,
                        intensity_level,
                        emotion_1_id,
                        `{X_COLS}`
                        FROM opensmile_functionals
                        WHERE mix = 0
                        AND video_id IN ('A223',
                                        'A220',
                                        'A91')
                        AND mode = 'v'
                        ;""".format(X_COLS=list2string(x_cols))

    # print(query)

    df, _ = execute_sql_pandas(query)

    df.to_csv(os.path.join(ROOT_DIR, "files/out/opensmile_functionals_query.csv"), index=False)


def opensmile_lld_query(x_cols):
    query = """SELECT filename,
                        video_id,
                        intensity_level,
                        emotion_1_id,
                        `{X_COLS}`
                        FROM opensmile_lld
                        WHERE mix = 0
                        AND video_id NOT IN ('A050121-R',
                                                'A21',
                                                'A34')
                        ;""".format(X_COLS=list2string(x_cols))

    # print(query)

    df, _ = execute_sql_pandas(query)

    df.to_csv(os.path.join(ROOT_DIR, "files/out/opensmile_lld_query.csv"), index=False)


def main():
    x_cols = [*AU_INTENSITY_COLS, *GAZE_COLS, *POSE_COLS]
    openface_query(x_cols)

    x_cols = AUDIO_FUNCTIONALS_EGEMAPS_COLS
    opensmile_functionals_query(x_cols)

    # x_cols = AUDIO_LLD_COLS
    # opensmile_lld_query(x_cols)


if __name__ == "__main__":
    main()
