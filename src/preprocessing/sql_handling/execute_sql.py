import pandas as pd
import time
from global_config import ROOT_DIR
import os

from src.preprocessing.sql_handling.connector import ConnectionHandler
from src.preprocessing.sql_handling.queries import query_audio_cols, query_au_cols

def execute_sql_pandas_chunks(query):
    queryExecStart = time.time()
    engine = ConnectionHandler.get_engine()
    print("executing query: \n{}".format(query))
    dfs = []
    for df in pd.read_sql(query, engine, chunksize=1000000):
        print("appending df with shape: " + str(df.shape))
        dfs.append(df)
        print("done")
    read_duration = round(time.time() - queryExecStart, 3)
    print("Read duration: {}".format(read_duration))
    ret = pd.concat(dfs)
    return ret, read_duration

def execute_sql_pandas(query):
    queryExecStart = time.time()
    engine = ConnectionHandler.get_engine()
    print("executing query: \n{}".format(query))
    df = pd.read_sql(query, engine)
    print("done")
    read_duration = round(time.time() - queryExecStart, 3)
    print("Read duration: {}".format(read_duration))
    return df, read_duration


def execute_sql(query):
    queryExecStart = time.time()
    engine = ConnectionHandler.get_engine()
    conn = engine.connect()
    print("executing query: \n{}".format(query))
    ret = conn.execute(query)
    print("done")
    read_duration = round(time.time() - queryExecStart, 3)
    print("Read duration: {}".format(read_duration))
    return ret, read_duration


def main():
    df, read_duration = execute_sql_pandas(query_audio_cols)
    df.to_csv(os.path.join(ROOT_DIR, "files/out/audio.csv"), index=False)


    # TODO: There is some bug with the number of rows being queried
    # df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/au_cols_without_confidence_filter.csv"))
    df, read_duration = execute_sql_pandas(query_au_cols)
    df.to_csv(os.path.join(ROOT_DIR, "files/out/au.csv"), index=False)


dfs, read_duration = execute_sql_pandas_chunks(query_audio_cols)

# if __name__ == '__main__':
#     main()
