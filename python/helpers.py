import re
from pathlib import Path
import logging
from glob import glob


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


def main():
    filepath = '../files/tests/csv_concat/A220_adm_p_1.csv'
    print(filepath)
    filename = get_filename(filepath)
    print(filename)

    print(Path(filepath).name)


if __name__ == "__main__":
    main()


