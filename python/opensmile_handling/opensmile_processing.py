import opensmile

import glob

from python.helpers import get_filename
from python.opensmile_handling.duplicate_handler import DuplicateHandler


smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.Functionals,
)


def process_files(out_path, file_path):
    duplicate_handler = DuplicateHandler(out_path)

    for file in glob.glob(file_path, recursive=True):
        filename = get_filename(file)
        if duplicate_handler.is_duplicate(filename):
            print("file: " + filename + " is duplicate, skipping...")
            continue
        else:
            print("file: " + filename + " is original, processing...")
            df = smile.process_file(file)
            df.to_csv(out_path + filename + ".csv")


def main():
    file_path = "../files/tests/videos/**/*.mov"
    out_path = "../../files/tests/videos/opensmile/"
    process_files(file_path, out_path)


if __name__ == "__main__":
    main()


