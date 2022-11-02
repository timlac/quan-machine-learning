import pandas as pd
import time
from global_config import ROOT_DIR

from src.preprocessing.sql_handling.connector import ConnectionHandler

from src.preprocessing.sql_handling.queries import query_au_cols_without_confidence_filter_A74


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
    ret = conn.execute(query)
    read_duration = round(time.time() - queryExecStart, 3)
    return ret, read_duration


def main():
    df, read_duration = execute_sql_pandas(query_au_cols_without_confidence_filter_A74)
    df.to_csv(ROOT_DIR + "/files/out/au_cols_a74.csv", index=False)






    # q = """SELECT * FROM openface LIMIT 10"""
    # df, read_duration = execute_sql_pandas(q)
    # print("pandas query executed in: {} seconds".format(read_duration))
    # print(df)

    # # a small test of execution time
    # # execution times are similar
    #
    # query = """SELECT filename,
    # video_id,
    # emotion_1,
    # emotion_1_id,
    # AU01_r,
    # AU02_r,
    # AU04_r,
    # AU05_r,
    # AU06_r,
    # AU07_r,
    # AU09_r,
    # AU10_r,
    # AU12_r,
    # AU14_r,
    # AU15_r,
    # AU17_r,
    # AU20_r,
    # AU23_r,
    # AU25_r,
    # AU26_r,
    # AU45_r
    # FROM openface
    # WHERE success = 1 AND confidence >= 0.98 AND mix = 0
    # AND video_id IN ('A101');"""
    #
    # # pandas query executed in: 51.318 seconds
    # df, read_duration = execute_sql_pandas(query)
    # print("pandas query executed in: {} seconds".format(read_duration))
    #
    # # raw query executed in: 54.673 seconds
    # df, read_duration = execute_sql(query)
    # print("raw query executed in: {} seconds".format(read_duration))


if __name__ == '__main__':
    main()
