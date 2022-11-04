from global_config import AUDIO_LLD_COLS, AU_INTENSITY_COLS, POSE_COLS


def list2string(lst):
    return "`, `".join(lst)


openface_query = """SELECT filename,
video_id,
emotion_1_id,
success,
confidence,
`{X_COLS}`
FROM openface
WHERE mix = 0;"""

specific_openface_query = """SELECT filename,
video_id,
emotion_1_id,
success,
confidence,
`{X_COLS}`
FROM openface
WHERE mix = 0
AND video_id = '{VIDEO_ID}';"""

opensmile_lld_query = """SELECT filename,
video_id,
emotion_1_id,
`{X_COLS}`
FROM opensmile_lld
WHERE mix = 0
LIMIT 1000;"""

# AU
query_au_cols = openface_query.format(X_COLS=list2string(AU_INTENSITY_COLS))
query_au_cols_A220 = specific_openface_query.format(X_COLS=list2string(AU_INTENSITY_COLS), VIDEO_ID="A220")
query_au_cols_A74 = specific_openface_query.format(X_COLS=list2string(AU_INTENSITY_COLS), VIDEO_ID="A74")

# POSE
query_pose_cols = openface_query.format(X_COLS=list2string(POSE_COLS))

# AUDIO
query_audio_cols = opensmile_lld_query.format(X_COLS=list2string(AUDIO_LLD_COLS))

