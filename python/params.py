
class Params:

    DEFAULT_INTENSITY_LEVEL = 1
    DEFAULT_VERSION = 1
    DEFAULT_SITUATION = 1

    # can be vocalization (v) or prosody (p)
    DEFAULT_MODE = "v"

    DEFAULT_PROPORTIONS = "0"
    DEFAULT_SECOND_EMOTION = None

    def __init__(self,
                 emotion_1: str,
                 emotion_2=DEFAULT_SECOND_EMOTION,
                 proportions=DEFAULT_PROPORTIONS,
                 mode=DEFAULT_MODE,
                 mix=False,
                 intensity_level=DEFAULT_INTENSITY_LEVEL,
                 version=DEFAULT_VERSION,
                 situation=DEFAULT_SITUATION):

        self.mix = mix
        self.emotion_1 = emotion_1
        self.emotion_2 = emotion_2
        self.proportions = proportions
        self.mode = mode
        self.intensity_level = intensity_level
        self.version = version
        self.situation = situation

    def set_column_values(self):
        for i in vars(self):
            print(i)


if __name__ == "__main__":
    input_path = "../files/tests/csv_concat/A220_adm_p_1.csv"

    name_list = ['A332', 'ang', 'p' '2']

    params = Params(emotion_1=name_list[1], mode=name_list[2], intensity_level=int(name_list[3]))

    params.set_column_values()
