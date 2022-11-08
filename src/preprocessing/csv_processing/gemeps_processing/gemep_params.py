import pandas as pd

from src.utils.helpers import get_digits_only, get_filename, get_csv_paths
from global_config import gemep_emotion_abr_to_emotion_id, ROOT_DIR


def get_emotion_id(emotion):
    return gemep_emotion_abr_to_emotion_id[emotion]


class GemepParams(object):

    def __init__(self,
                 filename,
                 video_id,
                 emotion, ):

        self.filename = filename
        self.video_id = video_id
        self.emotion = emotion
        self.emotion_id = get_emotion_id(emotion)

    def set_column_values(self, df):
        for key, value in vars(self).items():
            df[key] = value
        return df


def main():
    input_path = "/home/tim/work/su-thesis-project/datasets/GEMEP/gemep_opensmile_eGeMAPSv02_lowleveldescriptors/norm_A01des135.avi.csv"
    df = pd.read_csv(input_path)

    df = df.drop(columns="file")

    file_name = get_filename(input_path)
    video_id = file_name[5:8]  # Get actor number id
    emotion = file_name[8:11]  # Get emotion id
    _ = file_name[11:]  # Get number after emotion

    params = GemepParams(filename=file_name,
                         video_id=video_id,
                         emotion=emotion)

    df = params.set_column_values(df)


    df.to_csv(ROOT_DIR + "/files/tests/out/paramtest.csv", index=False)


if __name__ == "__main__":
    main()
