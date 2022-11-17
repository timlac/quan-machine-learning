import os

import numpy as np
import pandas as pd

from global_config import ROOT_DIR

from src.preprocessing.dataset_creation.helpers import slice_by, get_fixed_col


def group_creation_desc(video_ids, groups, group_mapper):
    video_ids_unique, video_ids_counts = np.unique(video_ids, return_counts=True)
    counts_per_video_id = dict(zip(video_ids_unique, video_ids_counts))

    groups_unique, groups_counts = np.unique(groups, return_counts=True)
    counts_per_group = dict(zip(groups_unique, groups_counts))

    print("Number of videos per video id:")
    print(counts_per_video_id)

    print("Group assignment:")
    print(group_mapper)

    print("Number of videos per group")
    print(counts_per_group)


def create_groups(video_ids, n_groups):
    """
    :param video_ids: np array with video id for every video
    :param n_groups: number of groups to create
    :return: np array with group assignment for every video, same shape as video_ids
    """
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