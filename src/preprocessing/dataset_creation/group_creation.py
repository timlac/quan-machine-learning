import random
from global_config import seed, ROOT_DIR


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
