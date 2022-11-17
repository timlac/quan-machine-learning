import os
import random

import numpy as np
import pandas as pd

from global_config import seed, ROOT_DIR
from sklearn.utils import shuffle

from src.preprocessing.dataset_creation.helpers import slice_by, get_fixed_col


def group_creation_desc(video_ids, groups, group_mapper):
    video_ids_unique, video_ids_counts = np.unique(video_ids, return_counts=True)
    counts_per_video_id = dict(zip(video_ids_unique, video_ids_counts))

    groups_unique, groups_counts = np.unique(groups, return_counts=True)
    counts_per_group = dict(zip(groups_unique, groups_counts))

    print("Group assignment:")
    print(group_mapper)

    print("Number of videos per video id:")
    print(counts_per_video_id)

    print("Number of videos per group")
    print(counts_per_group)


def create_groups(video_ids, n_groups):
    group_mapper = {}

    for idx, video_id in enumerate(np.unique(video_ids)):
        group_mapper[video_id] = idx % n_groups

    groups = []
    for video_id in video_ids:
        group = group_mapper[video_id]
        groups.append(group)

    groups = np.array(groups)

    group_creation_desc(video_ids, groups, group_mapper)

    if not groups.shape == video_ids.shape:
        raise ValueError("something went wrong, group vector size is not the same as video id vector")
    else:
        return groups


def main():
    df = pd.read_csv(os.path.join(ROOT_DIR, "files/out/query_13_videos.csv"))
    slices = slice_by(df, "filename")
    video_ids = get_fixed_col(slices, "video_id")
    groups = create_groups(video_ids, 5)


if __name__ == "__main__":
    main()

# TODO: Get rid of all of this and just create 5 groups with equal amount of video ids in them


def get_evens(size):
    ret = []
    for n in range(size):
        if n % 2 == 0:
            ret.append(n)
    return ret


def get_odds(size):
    ret = []
    for n in range(size):
        if n % 2 == 1:
            ret.append(n)
    return ret


def create_twinned_groups(filenames, number_of_groups=5):
    """
    :param filenames: pd.Series with all filenames in the dataset
    :param number_of_groups: the number of groups to create
    :return: dict with (filename: group)
    """
    groups = {}

    filenames = shuffle(filenames).reset_index(drop=True)

    i = 0
    while len(groups) < len(filenames):
        groups[filenames[i]] = i % number_of_groups
        i += 1

    return groups


def create_video_id_groups(video_ids):
    """
    :param video_ids: pd.Series with all unique video ids in the dataset.
    Videos that come from the same actor have the same video id.
    :return: dict with {video_id: group} such that there are 2 video ids for every group
    """
    length = len(video_ids)
    even_numbers = get_evens(length)
    odd_numbers = get_odds(length)

    odd_numbers_shuffled = random.sample(odd_numbers, len(odd_numbers))

    groups = {}
    # idx = 0,1,2,3,4...
    # even_number = 0,2,4,6...
    # assign video_id[0] to group 0, video_id[2] to group 1, video_id[4] to group 2 and so on
    for idx, even_number in enumerate(even_numbers):
        groups[video_ids[even_number]] = idx

    # idx = 0,1,2,3,4...
    # odd_number = 5, 3, 7, 1...
    # assign video_id[5] to group 0, video_id[3] to group 1, video_id[7] to group 2 and so on
    for idx, odd_number in enumerate(odd_numbers_shuffled):
        groups[video_ids[odd_number]] = idx

    return groups
