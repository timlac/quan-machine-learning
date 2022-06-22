from glob import glob
from tqdm import tqdm
from pathlib import Path
import pandas as pd
from params import Params

from python.helpers import get_filename, get_digits_only


class ErrorFileException(Exception):
    def __init__(self, filename, message="Filename {} contains error marker, skipping file"):
        self.filename = filename
        self.message = message
        super().__init__(self.message.format(self.filename))


# filenames with mixed emotions contains the word mix
# filenames with neutral emotion contains the word neu
special_cases = {
    "mixed_emotions": "mix",
    "neutral_emotion": "neu",
    "error": "e"
}


def create_dataframe(paths):
    """
    :param paths: paths to csv files
    :return: csv files concatenated into a large dataframe with columns set from filenames
    """
    df = pd.DataFrame()  # Initialize empty data frame

    for filename in tqdm(paths):
        try:
            df_tmp = pd.read_csv(filename)
            df_tmp = set_df_columns(df_tmp, filename)
            df = pd.concat([df, df_tmp])
        except ErrorFileException as e:
            print(e)
            continue
    return df


def set_df_columns(df, filename):
    """
    :param df: dataframe to set columns for
    :param filename: used for setting columns like emotion, intensity level etc.
    :return: dataframe with set columns
    """

    file_name = get_filename(filename)
    name_list = name2list(file_name)

    params = Params()
    params.filename = Path(filename).name
    params.video_id = name_list[0]

    if name_list[1] == special_cases["mixed_emotions"]:
        params.set_mixed_emotions(name_list)
    elif name_list[1] == special_cases["neutral_emotion"]:
        params.set_neutral_emotion(name_list)
    elif len(name_list) > 4:
        if name_list[4] == special_cases["error"]:
            raise ErrorFileException(filename)
        elif name_list[4].startswith("ver"):
            params.set_versioned_emotion(name_list)
        else:
            params.set_long_name(name_list)
    else:
        params.set_default_emotion(name_list)

    df = params.set_column_values(df)
    return params.set_column_values(df)


def get_csv_paths(path):
    csv_paths = glob(path + '*.csv')
    print("Files found:", len(csv_paths))
    return csv_paths


def name2list(file_name):
    return file_name.split("_")


def main():
    input_path = "../files/tests/csv_concat/"
    paths = get_csv_paths(input_path)
    print(paths)
    df = create_dataframe(paths)
    print("saving csv")
    df.to_csv("../files/tests/out/csv_concat_test.csv")


if __name__ == "__main__":
    main()
