import pandas as pd
from tqdm import tqdm
import logging
import sys
from dotenv import load_dotenv
import os

from python.sql_handling.connector import ConnectionHandler
from python.helpers import get_csv_paths

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Uploader:
    """
    Class for uploading data
    """

    def __init__(self, table_name):
        self.table_name = table_name
        self.engine = ConnectionHandler.get_engine()

    def insert_csv(self, file_path):
        logging.info("uploading file: " + str(file_path))

        sql_string = "LOAD DATA LOCAL INFILE '{}' " \
                     "INTO TABLE {} " \
                     "CHARACTER SET utf8 " \
                     "FIELDS TERMINATED BY ',' " \
                     "LINES TERMINATED BY '\\n' " \
                     "IGNORE 1 LINES; ".format(file_path, self.table_name)

        logging.info("executing sql: " + str(sql_string))

        self.engine.execute(sql_string)

    def upload_dir(self, directory):
        paths = get_csv_paths(directory)
        for filepath in paths:
            self.insert_csv(filepath)

    @staticmethod
    def main():

        # directory = "/home/tim/work/su-thesis-project/projects/video_analysis/files/openface/"
        load_dotenv()
        input_path = os.getenv("OPENFACE_PROCESSED")

        table_name = "openface"

        uploader = Uploader(table_name)
        uploader.upload_dir(input_path)


if __name__ == '__main__':
    Uploader.main()
