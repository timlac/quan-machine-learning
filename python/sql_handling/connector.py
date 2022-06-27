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
        return "{}:{}@{}/{}".format(username, password, endpoint, database)

    @staticmethod
    def test_connection():
        engine = ConnectionHandler.get_engine()
        engine.connect()

    @staticmethod
    def get_engine():
        connection_string = ConnectionHandler.get_connection_string()

        return db.create_engine('mysql+pymysql://' + connection_string, encoding='utf8')

    @staticmethod
    def main():
        engine = ConnectionHandler.get_engine()


if __name__ == '__main__':
    ConnectionHandler.test_connection()

