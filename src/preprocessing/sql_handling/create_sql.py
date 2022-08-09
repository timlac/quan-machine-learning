import pandas as pd
import logging
import sys
from dotenv import load_dotenv

from src.preprocessing.sql_handling.connector import ConnectionHandler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class TableCreator:

    def __init__(self, table_name, datatypes):
        self.table_name = table_name
        self.datatypes = datatypes
        self.engine = ConnectionHandler.get_engine()

    def create_table_based_on_csv(self, file_path):
        df = pd.read_csv(file_path)

        with self.engine.connect() as connection:
            # write Data Frame to sql
            df.to_sql(self.table_name, connection, if_exists='replace', index=False,
                      dtype=self.datatypes)

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
