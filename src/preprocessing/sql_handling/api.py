from dotenv import load_dotenv
import os

from src.preprocessing.sql_handling.create_sql import TableCreator
from src.preprocessing.sql_handling.upload_sql import Uploader
from src.preprocessing.sql_handling.datatypes import general_datatypes
from src.utils.helpers import get_csv_paths


class Api:

    def __init__(self, input_path, table_name):
        self.input_path = input_path
        self.table_name = table_name

    def create_table(self, datatypes):
        table_creator = TableCreator(table_name=self.table_name, datatypes=datatypes)

        paths = get_csv_paths(self.input_path)
        first_csv = paths[0]
        table_creator.create_table_based_on_csv(first_csv)

        table_creator.truncate()
        table_creator.set_indices()

    def upload_data(self):
        uploader = Uploader(table_name=self.table_name)
        uploader.upload_dir(directory=self.input_path)


def main():
    load_dotenv()

    input_path = os.getenv("OPENSMILE_FUNCTIONALS_PROCESSED")
    table_name = "opensmile_functionals"
    datatypes = general_datatypes

    api = Api(input_path=input_path, table_name=table_name)

    # api.create_table(datatypes)

    api.upload_data()


if __name__ == "__main__":
    main()
