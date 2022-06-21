from glob import glob
from tqdm import tqdm
from pathlib import Path
import re
import pandas as pd


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

DEFAULT_INTENSITY_LEVEL = 1
DEFAULT_VERSION = 1
DEFAULT_SITUATION = 1


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

    file_name = remove_extension(filename)
    name_list = name2list(file_name)

    df["video_id"] = name_list[0]
    df["file"] = Path(filename).name
    # some videos are recorded in multiple versions, set 1 as default for all videos
    df['version'] = DEFAULT_VERSION
    # neutral emotions are recorded in multiple situations, set 1 as default for all videos
    df['situation'] = DEFAULT_SITUATION
    # neutral emotions and mixed emotions have no intensity level set 1 as default for all videos
    df['intensity_level'] = DEFAULT_INTENSITY_LEVEL

    if name_list[1] == special_cases["mixed_emotions"]:
        df = set_mixed_emotions(df, name_list)
    elif name_list[1] == special_cases["neutral_emotion"]:
        df = set_default_emotion(df, name_list)
        df = set_neutral_emotion(df, name_list)
    elif len(name_list) > 4:
        if name_list[4] == special_cases["error"]:
            raise ErrorFileException(filename)
        elif name_list[4].startswith("ver"):
            df = set_default_emotion(df, name_list)
            df = set_versioned_emotion(df, name_list)
        else:
            df = set_long_name(df, name_list)
    else:
        df = set_default_emotion(df, name_list)
    return df


def get_csv_paths(path):
    csv_paths = glob(path + '*.csv')
    print("Files found:", len(csv_paths))
    return csv_paths


def remove_extension(file):
    return Path(file).stem


def name2list(file_name):
    return file_name.split("_")


def get_digits_only(mixed_string):
    """
    :param mixed_string: some string that may contain digits and characters
    :return: only digits
    """
    return re.sub("\\D", "", mixed_string)


def set_emotion(params):






def set_mixed_emotions(df, name_list):
    df["mix"] = True
    df['emotion_1'] = name_list[2]
    df['emotion_2'] = name_list[3]
    df['proportions'] = name_list[4]
    return df


def set_neutral_emotion(df, name_list):
    # remove all non-numeric characters from situation string, keep only the digit
    df['situation'] = get_digits_only(name_list[2])
    # neutral emotions have no intensity level, setting to 1 as default
    return df


def set_long_name(df, name_list):
    df["mix"] = False
    # concat the long name of the emotion
    df['emotion_1'] = "_".join((name_list[1], name_list[2]))
    df['vocalization'] = name_list[3]
    df['intensity_level'] = name_list[4]
    return df


def set_default_emotion(df, name_list):
    df["mix"] = False
    df['emotion_1'] = name_list[1]
    df['vocalization'] = name_list[2]
    df['intensity_level'] = name_list[3]
    return df


def set_versioned_emotion(df, name_list):
    df['version'] = get_digits_only(name_list[4])
    return df


def main():
    input_path = "../files/tests/csv_concat/"
    paths = get_csv_paths(input_path)
    print(paths)
    df = create_dataframe(paths)
    print("saving csv")
    df.to_csv("../files/tests/out/csv_concat_test.csv")


main()

