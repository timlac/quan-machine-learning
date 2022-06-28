import pandas as pd
import logging
import sys
from dotenv import load_dotenv
import os


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
            df.to_sql(self.table_name, connection, if_exists='replace', index=False)
            connection.close()

    def set_primary_keys(self, name, int_key, varchar_key):

        sql_string = "ALTER TABLE {} " \
                     "ADD CONSTRAINT {} " \
                     "PRIMARY KEY ({}, {}(255));".format(self.table_name, name, int_key, varchar_key)

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

        table_creator = TableCreator("openface")
        table_creator.create_table(paths[0])

        table_creator.truncate()
        table_creator.set_primary_keys("name_frame", "frame", "filename")


if __name__ == '__main__':
    TableCreator.main()
