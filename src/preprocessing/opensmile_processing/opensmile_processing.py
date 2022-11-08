import os.path

import opensmile

import glob

from src.utils.helpers import get_filename
from src.preprocessing.opensmile_processing.duplicate_handler import DuplicateHandler

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.ComParE_2016,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors_Deltas,
)


def process_files(file_path, out_path, limit=None):
    duplicate_handler = DuplicateHandler(out_path)

    n = 0

    for file in glob.glob(file_path, recursive=True):
        if limit:
            n += 1
            if n >= limit:
                print("limit reached at " + str(n) + " stopping")
                return True

        filename = get_filename(file)
        if duplicate_handler.is_duplicate(filename):
            print("file: " + filename + " is duplicate, skipping...")
            continue
        else:
            print("file: " + filename + " is original, processing...")
            df = smile.process_file(file)

            df.to_csv(out_path + filename + ".csv")


def main():
    print("in main")
    # file_path = "../files/tests/example_data/**/*.mov"
    # out_path = "../files/tests/example_data/opensmile/"

    # file_path = "/media/tim/Seagate Backup Plus Drive/Documents/**/*.mov"
    # out_path = "/media/tim/Seagate Backup Plus Drive/out_opensmile_eGeMAPSv02_lowleveldescriptors/"

    # GEMEP
    file_path = "/home/tim/work/su-thesis-project/datasets/GEMEP/ALLVIDEOS/*.wmv"
    out_path = "/home/tim/work/su-thesis-project/datasets/GEMEP/gemep_opensmile_compare_2016_lowleveldescriptors_deltas/"

    print(os.path.isdir(out_path))

    process_files(file_path, out_path)


if __name__ == "__main__":
    main()
