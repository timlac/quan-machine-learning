from pathlib import Path
import pandas as pd
import logging
import sys
import os
from dotenv import load_dotenv

from src.csv_processing.column_refactor import refactor_duplicate_columns, reorder
from src.csv_processing.params import Params
from src.utils.helpers import get_filename, get_csv_paths, name2list
from src.custom_exceptions.error_file_exception import ErrorFileException


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class CsvProcessor:

    # filenames with mixed emotions contains the word mix
    # filenames with neutral emotion contains the word neu
    special_cases = {
        "mixed_emotions": "mix",
        "neutral_emotion": "neu",
        "error": "e"
    }

    def __init__(self, save_to):
        self.save_to = save_to

    def process_files(self, directory):
        """
        :param directory: dir to process recursively
        :return: csv files concatenated into a large dataframe with columns set from filenames
        """

        paths = get_csv_paths(directory)

        for filepath in paths:
            try:
                logging.info("processing file: " + str(filepath))
                df = pd.read_csv(filepath)
                df = self.set_df_columns(df, filepath)
                df = refactor_duplicate_columns(df)
                df = reorder(df)

                logging.info("saving file to csv: " + str(filepath))

                df.to_csv(os.path.join(self.save_to, Path(filepath).name), index=False)

            except ErrorFileException as e:
                logging.info(e)
                continue

    def set_df_columns(self, df, filepath):
        """
        :param df: dataframe to set columns for
        :param filepath: used for setting columns like emotion, intensity level etc.
        :return: dataframe with set columns
        """
        # filename without extension
        filename = get_filename(filepath)
        name_list = name2list(filename)

        params = Params(filename=filename, video_id=name_list[0])

        if name_list[1] == self.special_cases["mixed_emotions"]:
            params.set_mixed_emotions(name_list)
        elif name_list[1] == self.special_cases["neutral_emotion"]:
            params.set_neutral_emotion(name_list)
        elif len(name_list) > 4:
            if name_list[4] == self.special_cases["error"]:
                raise ErrorFileException(filepath)
            elif name_list[4].startswith("ver"):
                params.set_versioned_emotion(name_list)
            else:
                params.set_long_name(name_list)
        else:
            params.set_default_emotion(name_list)

        params.set_emotion_ids()
        df = params.set_column_values(df)
        return df

    def get_save_string(self, name):
        return os.path.join(self.save_to, name)


def main():
    load_dotenv()

    input_path = os.getenv("OPENSMILE_FUNCTIONAlS_RAW")
    save_to = os.getenv("OPENSMILE_FUNCTIONALS_PROCESSED")

    logging.info("Input path: " + str(input_path))

    csv_preprocessor = CsvProcessor(save_to)
    csv_preprocessor.process_files(input_path)


if __name__ == "__main__":
    main()
