import re
from pathlib import Path
import logging
from glob import glob
from global_config import emotion_id_to_emotion_abr


def get_filename(file):
    """
    :param file: some file path
    :return: filename without path or extension
    """
    return Path(file).stem


def get_digits_only(mixed_string):
    """
    :param mixed_string: some string that may contain digits and characters
    :return: only digits
    """
    return re.sub("\\D", "", mixed_string)


def get_csv_paths(path):
    csv_paths = glob(path + '*.csv')
    logging.info("Files found:" + str(len(csv_paths)))
    return csv_paths


def name2list(file_name):
    return file_name.split("_")


def hasher(value):
    hash32 = hash(value) & 0xffffffff
    return hash32


def mapper(input_values, mapper_dict):
    ret = []
    for i in input_values:
        ret.append(mapper_dict[i])
    return ret


def get_emotion_abrs_from_ids(emotion_ids):
    ret = []
    for i in emotion_ids:
        ret.append(emotion_id_to_emotion_abr[i])
    return ret


def main():
    # filepath = '../files/tests/csv_concat/A220_adm_p_1.csv'
    # print(filepath)
    # filename = get_filename(filepath)
    # print(filename)
    #
    # print(Path(filepath).name)

    emotion_ids = [1, 3, 4, 5, 7, 12, 17]
    abrs = get_emotion_abrs_from_ids(emotion_ids)
    print(abrs)



if __name__ == "__main__":
    main()
