import pandas as pd
import logging
import sys
from dotenv import load_dotenv
import os
import sqlalchemy as db

from src.sql_handling.connector import ConnectionHandler

from src.helpers import get_csv_paths

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class TableCreator:

    def __init__(self, table_name):
        self.table_name = table_name
        self.engine = ConnectionHandler.get_engine()

    def create_table(self, file_path):
        df = pd.read_csv(file_path)

        with self.engine.connect() as connection:
            # write Data Frame to sql
            df.to_sql(self.table_name, connection, if_exists='replace', index=False,
                      dtype={"filename": db.types.VARCHAR(length=32),
                             "frame": db.types.INT(),
                             "confidence": db.types.INT(),
                             "success": db.types.INT(),
                             "face_id": db.types.INT(),
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
                             'situation': db.types.INT()})

            connection.close()

    def set_indices(self):
        # sql_string = "ALTER TABLE {} ADD INDEX (success, confidence, mix);".format(self.table_name)
        #
        # self.engine.execute(sql_string)

        sql_string = "ALTER TABLE {} ADD INDEX (success, confidence, mix, video_id, emotion_1);".format(self.table_name)

        self.engine.execute(sql_string)


    def truncate(self):
        """Remove all data from table"""
        self.engine.execute("TRUNCATE TABLE {};".format(self.table_name))

    @staticmethod
    def main():
        load_dotenv()
        table_creator = TableCreator("openface")

        # openface_processed = os.getenv("OPENFACE_PROCESSED")
        # paths = get_csv_paths(openface_processed)
        # table_creator.create_table(paths[0])
        #
        # table_creator.truncate()


        table_creator.set_indices()



if __name__ == '__main__':
    TableCreator.main()
