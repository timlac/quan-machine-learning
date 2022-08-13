import argparse
import time
from dotenv import load_dotenv
from pathlib import Path
from src.learning.elastic_net import ElasticNet
from src.learning.knn import KNN
from src.learning.decision_tree import DecisionTree
from src.learning.random_forrest import RandomForest

from src.learning.load_data import DataLoader
from src.learning.save_output import Saver
import datetime

import os
import sys


def method_handler(method, data, test=False):
    # get the start time
    st = time.time()

    if method == "elastic_net":
        clf = ElasticNet.param_search(data=data, test=test)
    elif method == "knn":
        knn = KNN(data=data)
        clf = knn.param_search(test=test)
    elif method == "decision_tree":
        decision_tree = DecisionTree(data=data)
        clf = decision_tree.param_search(test=test)
    elif method == "rf":
        clf = RandomForest.param_search(data, test=test)
    else:
        raise RuntimeError

    # get the end time
    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print('Execution time:', str(datetime.timedelta(seconds=elapsed_time)))

    return clf


def main():
    # Create the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("source", choices=["audio", "video"])
    parser.add_argument("method", choices=["elastic_net", "knn", "decision_tree", "rf"])

    # Execute the parse_args() method
    args = parser.parse_args()

    load_dotenv()

    source = args.source
    method = args.method

    print("running {}".format(method))

    if source == "audio":
        out = os.getenv("AUDIO_OUT")
        input_file = os.path.join(out, "audio_data_egemaps_train.csv")
        filename_out = "egemaps_audio"
    elif source == "video":
        out = os.getenv("VIDEO_OUT")
        input_file = os.path.join(out, "video_data_intensity_train.csv")
        filename_out = "intensity_video"
    else:
        raise RuntimeError

    print("input file: {}".format(input_file))
    print("save location: {}".format(out))

    data = DataLoader(input_file)
    clf = method_handler(method, data)

    saver = Saver(clf=clf, method=method, n_groups=data.n_groups, save_location=out,
                  filename=filename_out)
    saver.save()


if __name__ == "__main__":
    main()
