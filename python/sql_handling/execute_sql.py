import pandas as pd


from python.sql_handling.connector import ConnectionHandler


def execute_sql_pandas(query):
    engine = ConnectionHandler.get_engine()
    df = pd.read_sql(query, engine)
    return df


def execute_sql(query):
    engine = ConnectionHandler.get_engine()
    conn = engine.connect()
    ret = conn.execute(query)
    return ret
