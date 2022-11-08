import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv


from src.utils.helpers import get_csv_paths, get_filename
from src.preprocessing.csv_processing.gemeps_processing.gemep_params import GemepParams


def process_files(directory, save_to):
    csv_paths = get_csv_paths(directory)

    for file_path in csv_paths:
        print("processing file: " + str(file_path))

        df = pd.read_csv(file_path)
        df = df.drop(columns="file")

        file_name = get_filename(file_path)
        video_id = file_name[5:8]  # Get actor number id
        emotion = file_name[8:11]  # Get emotion id
        _ = file_name[11:]  # Get number after emotion

        params = GemepParams(filename=file_name,
                             video_id=video_id,
                             emotion=emotion)

        df = params.set_column_values(df)

        df.to_csv(os.path.join(save_to, Path(file_path).name), index=False)


def main():

    load_dotenv()

    input_path = "/home/tim/work/su-thesis-project/datasets/GEMEP/gemep_opensmile_compare_2016_lowleveldescriptors/"
    save_to = os.getenv("GEMEP_OPENSMILE_COMPARE_LLD_PROCESSED")

    process_files(input_path, save_to)


if __name__ == "__main__":
    main()
