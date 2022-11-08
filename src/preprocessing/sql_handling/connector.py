import sqlalchemy as db
import os
from dotenv import load_dotenv


class ConnectionHandler:

    @staticmethod
    def get_connection_string():
        load_dotenv()
        endpoint = os.getenv("DB_ENDPOINT")
        database = os.getenv("DB_NAME")
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        return "{}:{}@{}/{}?{}".format(username, password, endpoint, database, "local_infile=1")

    @staticmethod
    def test_connection():
        engine = ConnectionHandler.get_engine()
        ret = engine.connect()

    @staticmethod
    def get_engine():
        connection_string = ConnectionHandler.get_connection_string()

        return db.create_engine('mysql+pymysql://' + connection_string, encoding='utf8', server_side_cursors=True)

    @staticmethod
    def main():
        engine = ConnectionHandler.get_engine()


if __name__ == '__main__':
    ConnectionHandler.test_connection()

