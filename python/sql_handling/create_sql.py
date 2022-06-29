import pandas as pd
import logging
import sys
from dotenv import load_dotenv
import os
import sqlalchemy as db

from python.sql_handling.connector import ConnectionHandler

from python.helpers import get_csv_paths

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
                      dtype={"filekey": db.types.BIGINT(),
                             "filename": db.types.VARCHAR(length=32),
                             "frame": db.types.INT(),
                             "confidence": db.types.INT(),
                             "success": db.types.INT(),
                             "face_id": db.types.INT(),
                             "video_id": db.types.VARCHAR(length=10),
                             "emotion_1": db.types.VARCHAR(length=10),
                             'emotion_2': db.types.VARCHAR(length=10),
                             "mode": db.types.VARCHAR(length=1),
                             'mix': db.types.INT(),
                             'proportions': db.types.INT(),
                             'intensity_level': db.types.INT(),
                             'version': db.types.INT(),
                             'situation': db.types.INT()})

            connection.close()

    def set_primary_keys(self, name, key1, key2):
        sql_string = "ALTER TABLE {} " \
                     "ADD CONSTRAINT {} " \
                     "PRIMARY KEY ({}, {});".format(self.table_name, name, key1, key2)

        logging.info("executing sql: " + str(sql_string))

        self.engine.execute(sql_string)

    def truncate(self):
        """Remove all data from table"""
        self.engine.execute("TRUNCATE TABLE {};".format(self.table_name))

    @staticmethod
    def main():
        load_dotenv()
        openface_processed = os.getenv("OPENFACE_PROCESSED")
        paths = get_csv_paths(openface_processed)

        table_creator = TableCreator("openface_reduced")
        table_creator.create_table(paths[0])

        table_creator.truncate()
        table_creator.set_primary_keys("name_frame", "frame", "filekey")


if __name__ == '__main__':
    TableCreator.main()
