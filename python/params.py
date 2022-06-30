import pandas as pd

from python.helpers import get_digits_only, hasher
from python.global_config import emotion_abr_to_emotion_id


class Params(object):
    DEFAULT_INTENSITY_LEVEL = 1
    DEFAULT_VERSION = 1
    DEFAULT_SITUATION = 1

    # can be vocalization (v) or prosody (p)
    DEFAULT_MODE = "v"

    DEFAULT_PROPORTIONS = 0
    DEFAULT_SECOND_EMOTION = None
    DEFAULT_MIX = 0
    # set it to some number not in the list
    DEFAULT_EMOTION_ID = 100

    def __init__(self,
                 filename,
                 video_id,
                 emotion_1=None,
                 emotion_2=DEFAULT_SECOND_EMOTION,
                 emotion_1_id=DEFAULT_EMOTION_ID,
                 emotion_2_id=DEFAULT_EMOTION_ID,
                 proportions=DEFAULT_PROPORTIONS,
                 mode=DEFAULT_MODE,
                 mix=DEFAULT_MIX,
                 intensity_level=DEFAULT_INTENSITY_LEVEL,
                 version=DEFAULT_VERSION,
                 situation=DEFAULT_SITUATION):

        self.filename = filename
        self.video_id = video_id
        self.mix = mix
        self.emotion_1 = emotion_1
        self.emotion_1_id = emotion_1_id
        self.emotion_2 = emotion_2
        self.emotion_2_id = emotion_2_id
        self.proportions = proportions
        self.mode = mode
        self.intensity_level = intensity_level
        self.version = version
        self.situation = situation

    def set_mixed_emotions(self, name_list):
        """
        e.g. A220_mix_ang_disg_5050.csv
        """
        self.mix = 1
        self.emotion_1 = name_list[2]
        self.emotion_2 = name_list[3]
        self.proportions = name_list[4]

    def set_neutral_emotion(self, name_list):
        """
        e.g. A220_neu_sit1_v.csv
        """
        self.emotion_1 = name_list[1]
        # remove all non-numeric characters from situation string, keep only the digit
        self.situation = get_digits_only(name_list[2])
        self.mode = name_list[3]

    def set_long_name(self, name_list):
        """
        e.g. A220_neg_sur_p_1.csv
        """
        # concat the long name of the emotion
        self.emotion_1 = "_".join((name_list[1], name_list[2]))
        self.mode = name_list[3]
        self.intensity_level = name_list[4]

    def set_default_emotion(self, name_list):
        """
        e.g. A220_adm_p_1.csv
        """
        self.emotion_1 = name_list[1]
        self.mode = name_list[2]
        self.intensity_level = name_list[3]

    def set_versioned_emotion(self, name_list):
        """
        e.g. A327_ang_v_1_ver1.csv
        """
        self.emotion_1 = name_list[1]
        self.mode = name_list[2]
        self.intensity_level = name_list[3]
        self.version = get_digits_only(name_list[4])

    def set_emotion_ids(self):
        self.emotion_1_id = emotion_abr_to_emotion_id[self.emotion_1]
        if self.mix == 1:
            self.emotion_2_id = emotion_abr_to_emotion_id[self.emotion_2]

    def set_column_values(self, df):
        for key, value in vars(self).items():
            df[key] = value
        return df


def main():
    input_path = "../files/tests/csv_concat/A220_adm_p_1.csv"
    df = pd.read_csv(input_path)

    name_list = ['A332', 'ang', 'p', '2']

    params = Params(filename=input_path,
                    video_id=name_list[0],
                    emotion_1=name_list[1],
                    mode=name_list[2],
                    intensity_level=int(name_list[3]))

    params.set_emotion_ids()
    df = params.set_column_values(df)
    df.to_csv("../files/tests/out/paramtest.csv")


if __name__ == "__main__":
    main()
