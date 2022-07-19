import sqlalchemy as db

general_datatypes = {"filename": db.types.VARCHAR(length=32),
             "video_id": db.types.VARCHAR(length=10),
             "emotion_1": db.types.VARCHAR(length=10),
             'emotion_2': db.types.VARCHAR(length=10),
             "emotion_1_id": db.types.INT(),
             'emotion_2_id': db.types.INT(),
             "mode": db.types.VARCHAR(length=1),
             'mix': db.types.INT(),
             'proportions': db.types.INT(),
             'intensity_level': db.types.INT(),
             'version': db.types.INT(),
             'situation': db.types.INT()}

specific_openface_datatypes = {"frame": db.types.INT(),
                               "confidence": db.types.INT(),
                               "success": db.types.INT(),
                               "face_id": db.types.INT()}

openface_datatypes = dict(general_datatypes, **specific_openface_datatypes)
