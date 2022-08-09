import matplotlib.colors
import seaborn as sns

threads = -20


# Color palette
blue_rgb       = (78/255,  121/255, 167/255)
orange_rgb     = (242/255, 142/255, 43/255)
red_rgb        = (225/255, 87/255,  89/255)
turquoise_rgb  = (118/255, 183/255, 178/255)
green_rgb      = (89/255,  161/255, 79/255)
yellow_rgb     = (237/255, 201/255, 72/255)
purple_rgb     = (176/255, 122/255, 161/255)
pink_rgb       = (255/255, 157/255, 167/255)
brown_rgb      = (156/255, 117/255, 95/255)
gray_rgb       = (186/255, 176/255, 172/255)

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
blue_shades = [(78/255,  121/255, 167/255),
               (163/255, 201/255, 220/255)]

# More color definitions
conf_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(255/255,255/255,215/255), turquoise_rgb, blue_rgb])
pos_cmap =  matplotlib.colors.LinearSegmentedColormap.from_list("", [(205/255,242/255,246/255),(23/255,39/255,82/255)])
neg_pos_cmap =  matplotlib.colors.LinearSegmentedColormap.from_list("", [blue_rgb,orange_rgb])

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
n_folds = 5

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
