import re
from pathlib import Path


def get_filename(file):
    return Path(file).stem


def main():
    filepath = '../files/tests/csv_concat/A220_adm_p_1.csv'
    print(filepath)
    filename = get_filename(filepath)
    print(filename)


if __name__ == "__main__":
    main()


def get_digits_only(mixed_string):
    """
    :param mixed_string: some string that may contain digits and characters
    :return: only digits
    """
    return re.sub("\\D", "", mixed_string)
