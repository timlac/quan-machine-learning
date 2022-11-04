import matplotlib.colors
import seaborn as sns
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

threads = -20

# Color palette
blue_rgb = (78 / 255, 121 / 255, 167 / 255)
orange_rgb = (242 / 255, 142 / 255, 43 / 255)
red_rgb = (225 / 255, 87 / 255, 89 / 255)
turquoise_rgb = (118 / 255, 183 / 255, 178 / 255)
green_rgb = (89 / 255, 161 / 255, 79 / 255)
yellow_rgb = (237 / 255, 201 / 255, 72 / 255)
purple_rgb = (176 / 255, 122 / 255, 161 / 255)
pink_rgb = (255 / 255, 157 / 255, 167 / 255)
brown_rgb = (156 / 255, 117 / 255, 95 / 255)
gray_rgb = (186 / 255, 176 / 255, 172 / 255)

sns_saturation = 1

palette_def = [blue_rgb,
               orange_rgb,
               red_rgb,
               turquoise_rgb,
               green_rgb,
               yellow_rgb,
               purple_rgb,
               pink_rgb,
               brown_rgb,
               gray_rgb]

# Blues (2 shades)
blue_shades = [(78 / 255, 121 / 255, 167 / 255),
               (163 / 255, 201 / 255, 220 / 255)]

# More color definitions
conf_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(255 / 255, 255 / 255, 215 / 255), turquoise_rgb,
                                                                     blue_rgb])
pos_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(205 / 255, 242 / 255, 246 / 255),
                                                                    (23 / 255, 39 / 255, 82 / 255)])
neg_pos_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [blue_rgb, orange_rgb])

# Style definitions
sns.set_style({'axes.facecolor': 'white',
               'axes.edgecolor': '.8',
               'axes.grid': True,
               'axes.axisbelow': True,
               'axes.labelcolor': '.15',
               'figure.facecolor': 'white',
               'grid.color': '.8',
               'grid.linestyle': '-',
               'text.color': '.15',
               'xtick.color': '.15',
               'ytick.color': '.15',
               'xtick.direction': 'out',
               'ytick.direction': 'out',
               'lines.solid_capstyle': 'round',
               'patch.edgecolor': 'w',
               'image.cmap': 'rocket',
               'font.family': ['sans-serif'],
               'font.sans-serif': ['Arial',
                                   'DejaVu Sans',
                                   'Liberation Sans',
                                   'Bitstream Vera Sans',
                                   'sans-serif'],
               'patch.force_edgecolor': False,
               'xtick.bottom': False,
               'xtick.top': False,
               'ytick.left': False,
               'ytick.right': False,
               'axes.spines.left': False,
               'axes.spines.bottom': True,
               'axes.spines.right': False,
               'axes.spines.top': False}
              )
matplotlib.rcParams.update({'font.size': 10})

# Seed
seed = 27

# Number of folder CV
# n_folds = 5

# Mapping emotions
emotion_abr_to_emotion = {
    "reg": "regret",
    "conf": "confusion",
    "det": "determination",
    "dou": "doubt",
    "env": "envy",
    "adm": "admiration",
    "sad": "sadness",
    "gra": "gratitude",
    "ele": "elevation_rejoicing",
    "pos_sur": "positive_surprise",
    "fea": "fear",
    "neg_sur": "negative_surprise",
    "ang": "anger",
    "amu": "amusement",
    "rej": "rejection",
    "scha": "schadenfreude",
    "sat": "satisfaction_contentment",
    "dist": "distress_pain",
    "awe": "awe",
    "ins": "inspiration",
    "tri": "triumph_achievement",
    "hop": "hope",
    "neu": "neutral",
    "ple": "sensory_pleasure",
    "sex": "sexual_lust",
    "pea": "peacefulness_serenity",
    "bor": "boredom",
    "conc": "concentration",
    "ten": "satisfaction_contentment",
    "int": "interest_curiosity",
    "nos": "nostalgia",
    "sar": "sarcasm",
    "cont": "contempt",
    "hap": "happiness_joy",
    "anx": "anxiety",
    "disg": "disgust",
    "exc": "excitement_expectation",
    "disa": "disappointment",
    "rel": "relief",
    "emb": "embarrassment",
    "gui": "guilt",
    "pri": "pride",
    "mov": "being moved",
    "sha": "shame",
}

emotion_to_emotion_abr = dict(zip(emotion_abr_to_emotion.values(), emotion_abr_to_emotion.keys()))

# mapping emotions to id numbers
emotion_abr_to_emotion_id = {'reg': 0,
                             'conf': 1,
                             'det': 2,
                             'dou': 3,
                             'env': 4,
                             'adm': 5,
                             'sad': 6,
                             'gra': 7,
                             'ele': 8,
                             'pos_sur': 9,
                             'fea': 10,
                             'neg_sur': 11,
                             'ang': 12,
                             'amu': 13,
                             'rej': 14,
                             'scha': 15,
                             'sat': 16,
                             'dist': 17,
                             'awe': 18,
                             'ins': 19,
                             'tri': 20,
                             'hop': 21,
                             'neu': 22,
                             'ple': 23,
                             'sex': 24,
                             'pea': 25,
                             'bor': 26,
                             'conc': 27,
                             'ten': 28,
                             'int': 29,
                             'nos': 30,
                             'sar': 31,
                             'cont': 32,
                             'hap': 33,
                             'anx': 34,
                             'disg': 35,
                             'exc': 36,
                             'disa': 37,
                             'rel': 38,
                             'emb': 39,
                             'gui': 40,
                             'pri': 41,
                             'mov': 42,
                             'sha': 43}

emotion_id_to_emotion_abr = dict(zip(emotion_abr_to_emotion_id.values(), emotion_abr_to_emotion_id.keys()))

emotion_id_to_emotion = {0: "regret",
                         1: "confusion",
                         2: "determination",
                         3: "doubt",
                         4: "envy",
                         5: "admiration",
                         6: "sadness",
                         7: "gratitude",
                         8: "elevation_rejoicing",
                         9: "positive_surprise",
                         10: "fear",
                         11: "negative_surprise",
                         12: "anger",
                         13: "amusement",
                         14: "rejection",
                         15: "schadenfreude",
                         16: "satisfaction_contentment",
                         17: "distress_pain",
                         18: "awe",
                         19: "inspiration",
                         20: "triumph_achievement",
                         21: "hope",
                         22: "neutral",
                         23: "sensory_pleasure",
                         24: "sexual_lust",
                         25: "peacefulness_serenity",
                         26: "boredom",
                         27: "concentration",
                         28: "satisfaction_contentment",
                         29: "interest_curiosity",
                         30: "nostalgia",
                         31: "sarcasm",
                         32: "contempt",
                         33: "happiness_joy",
                         34: "anxiety",
                         35: "disgust",
                         36: "excitement_expectation",
                         37: "disappointment",
                         38: "relief",
                         39: "embarrassment",
                         40: "guilt",
                         41: "pride",
                         42: "being moved",
                         43: "shame"}

emotion_to_emotion_id = dict(zip(emotion_id_to_emotion.values(), emotion_id_to_emotion.keys()))

basic_emotions = {
    "sad": "sadness",
    "fea": "fear",
    "ang": "anger",
    "int": "interest_curiosity",
    "hap": "happiness_joy",
    "disg": "disgust",
    "gui": "guilt",
    "sha": "shame",
}

AU_INTENSITY_COLS = ['AU01_r',
                     'AU02_r',
                     'AU04_r',
                     'AU05_r',
                     'AU06_r',
                     'AU07_r',
                     'AU09_r',
                     'AU10_r',
                     'AU12_r',
                     'AU14_r',
                     'AU15_r',
                     'AU17_r',
                     'AU20_r',
                     'AU23_r',
                     'AU25_r',
                     'AU26_r',
                     'AU45_r']

au_intensity_name_to_index = {'AU01_r': 0,
                              'AU02_r': 1,
                              'AU04_r': 2,
                              'AU05_r': 3,
                              'AU06_r': 4,
                              'AU07_r': 5,
                              'AU09_r': 6,
                              'AU10_r': 7,
                              'AU12_r': 8,
                              'AU14_r': 9,
                              'AU15_r': 10,
                              'AU17_r': 11,
                              'AU20_r': 12,
                              'AU23_r': 13,
                              'AU25_r': 14,
                              'AU26_r': 15,
                              'AU45_r': 16}

index_to_au_intensity_name = dict(zip(au_intensity_name_to_index.values(), au_intensity_name_to_index.keys()))

au_intensity_name_to_desc = {'AU01_r': "AU01 (inner brow raiser)",
                             'AU02_r': "AU02 (outer brow raiser)",
                             'AU04_r': "AU04 (brow lowerer)",
                             'AU05_r': "AU05 (upper lid raiser)",
                             'AU06_r': "AU06 (cheek raiser)",
                             'AU07_r': "AU07 (lid tightener)",
                             'AU09_r': "AU09 (nose wrinkler)",
                             'AU10_r': "AU10 (upper lip raiser)",
                             'AU12_r': "AU12 (lip corner puller)",
                             'AU14_r': "AU14 (dimpler)",
                             'AU15_r': "AU15 (lip corner depressor)",
                             'AU17_r': "AU17 (chin raiser)",
                             'AU20_r': "AU20 (lip stretcher)",
                             'AU23_r': "AU23 (lip tightener)",
                             'AU25_r': "AU25 (lips part)",
                             'AU26_r': "AU26 (jaw drop)",
                             'AU45_r': "AU45 (blink)"
                             }

desc_to_au_intensity_name = dict(zip(au_intensity_name_to_desc.values(), au_intensity_name_to_desc.keys()))

POSE_COLS = [
    "pose_Rx",
    "pose_Ry",
    "pose_Rz",
    "pose_Tx",
    "pose_Ty",
    "pose_Tz"
]

AUDIO_LLD_COLS = [
    "Loudness_sma3",
    "alphaRatio_sma3",
    "hammarbergIndex_sma3",
    "slope0-500_sma3",
    "slope500-1500_sma3",
    "spectralFlux_sma3",
    "mfcc1_sma3", "mfcc2_sma3",
    "mfcc3_sma3", "mfcc4_sma3",
    "F0semitoneFrom27.5Hz_sma3nz",
    "jitterLocal_sma3nz",
    "shimmerLocaldB_sma3nz",
    "HNRdBACF_sma3nz",
    "logRelF0-H1-H2_sma3nz",
    "logRelF0-H1-A3_sma3nz",
    "F1frequency_sma3nz",
    "F1bandwidth_sma3nz",
    "F1amplitudeLogRelF0_sma3nz",
    "F2frequency_sma3nz",
    "F2bandwidth_sma3nz",
    "F2amplitudeLogRelF0_sma3nz",
    "F3frequency_sma3nz",
    "F3bandwidth_sma3nz",
    "F3amplitudeLogRelF0_sma3nz"
]

TARGET_COLUMN = "emotion_1_id"
