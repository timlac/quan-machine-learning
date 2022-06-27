import pandas as pd
from python.sql_handling.connector import ConnectionHandler


class EasyUpload:
    """
    Class for uploading data
    """

    def __init__(self):
        self.engine = ConnectionHandler.get_engine()

    def append_to_sql(self, df, filename, file_path):
        table_name = self.trim_table_name(filename)

        with self.engine.connect() as connection:
            # write Data Frame to sql
            df.to_sql(table_name, connection, if_exists='replace', index=False)
            connection.close()
        self.truncate(table_name)
        self.insert_csv(file_path, table_name)


    def create_table(self, file_path, table_name):
        df = pd.read_csv(file_path)

        df = self.refactor_duplicate_columns(df)

        with self.engine.connect() as connection:
            # write Data Frame to sql
            df.to_sql(table_name, connection, if_exists='replace', index=False)
            connection.close()

    def insert_csv(self, file_path, table_name):

        sql_string = "LOAD DATA LOCAL INFILE '{}' " \
                     "INTO TABLE {} " \
                     "CHARACTER SET utf8 " \
                     "FIELDS TERMINATED BY ',' " \
                     "LINES TERMINATED BY '\\n' " \
                     "IGNORE 1 LINES; ".format(file_path, table_name)

        print(sql_string)

        self.engine.execute(sql_string)

    def truncate(self, table_name):
        """Remove everything except column definitions from table"""
        self.engine.execute("TRUNCATE TABLE {};".format(table_name))

    def trim_table_name(self, filename):
        table_name = filename.replace("_SE_20191114_1.csv", "")
        return table_name.lower()

    def read_folder(self, dir, nrows):
        import os
        for filename in os.listdir(dir):
            if filename.endswith(".csv"):
                file_path = os.path.join(dir, filename)
                df = pd.read_csv(file_path, nrows=nrows)
                self.append_to_sql(df, filename, file_path)
            else:
                continue

    @staticmethod
    def main():
        easy_upload = EasyUpload()
        # easy_upload.create_table("/home/tim/work/su-thesis-project/projects/video_analysis/files/tests/out/csv_concat_test.csv",
        #     "openface")

        easy_upload.truncate("openface")

        # easy_upload.insert_csv(
        #     "/home/tim/work/su-thesis-project/projects/video_analysis/files/tests/out/csv_concat.csv",
        #     "openface")


if __name__ == '__main__':
    EasyUpload.main()
