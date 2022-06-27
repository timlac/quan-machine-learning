from glob import glob
from tqdm import tqdm
from pathlib import Path
import pandas as pd
import logging
import sys

from python.column_refactor import refactor_duplicate_columns
from python.params import Params
from python.helpers import get_filename, get_digits_only
from python.sql_handling.upload import EasyUpload


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class ErrorFileException(Exception):
    def __init__(self, filename, message="\nFilename {} contains error marker, skipping file"):
        self.filename = filename
        self.message = message
        super().__init__(self.message.format(self.filename))


class Concatenator:

    # filenames with mixed emotions contains the word mix
    # filenames with neutral emotion contains the word neu
    special_cases = {
        "mixed_emotions": "mix",
        "neutral_emotion": "neu",
        "error": "e"
    }

    def __init__(self):
        






# filenames with mixed emotions contains the word mix
# filenames with neutral emotion contains the word neu
special_cases = {
    "mixed_emotions": "mix",
    "neutral_emotion": "neu",
    "error": "e"
}


def iterate_files(paths, batch_size=382):
    """
    :param paths: paths to csv files
    :param batch_size
    :return: csv files concatenated into a large dataframe with columns set from filenames
    """
    easy_upload = EasyUpload()
    table_name = "openface"

    all_dfs = []

    for i in tqdm(range(0, len(paths), batch_size)):
        try:
            df = pd.read_csv(filename)
            df = set_df_columns(df, filename)
            df = refactor_duplicate_columns(df)

            all_dfs.append(df)

        except ErrorFileException as e:
            logging.info(e)
            continue

        df = pd.concat(all_dfs)
        df.to_csv()


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
    return df


def get_csv_paths(path):
    csv_paths = glob(path + '*.csv')
    logging.info("Files found:" + str(len(csv_paths)))
    return csv_paths


def name2list(file_name):
    return file_name.split("_")


def main():
    input_path = "/home/tim/Videos/out/"
    # out_path = "files/tests/out/csv_concat_test.csv"

    # input_path = "/media/tim/Seagate Backup Plus Drive/Out/"
    # out_path = "files/openface/csv_concat_openface.csv"

    logging.info("Input path: " + str(input_path))

    paths = get_csv_paths(input_path)
    logging.info("found paths: \n" + str(paths))
    iterate_files(paths)


if __name__ == "__main__":
    main()
