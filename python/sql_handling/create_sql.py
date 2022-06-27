import pandas as pd

from python.sql_handling.connector import ConnectionHandler


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

    def truncate(self):
        """Remove everything except column definitions from table"""
        self.engine.execute("TRUNCATE TABLE {};".format(self.table_name))

    @staticmethod
    def main():
        table_creator = TableCreator("openface")
        table_creator.create_table(
            "/home/tim/work/su-thesis-project/projects/video_analysis/files/openface/A334_anx_p_2.csv")

        table_creator.truncate()


if __name__ == '__main__':
    TableCreator.main()
