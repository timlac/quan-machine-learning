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


def create_groups(video_ids):
    """
    :param video_ids: All unique video ids in the dataset. Videos that come from the same actor have the same video id.
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


# video_ids = train_scaled_df.video_id.unique()
#
# # Find random pairs of video_ids
# random.seed(seed)
#
# # a list of even numbers
# video_ids_1 = get_evens(len(video_ids))
#
# # a list of odd numbers
# video_ids_2 = get_odds(len(video_ids))
#
# # shuffle the odd numbers
# video_ids_2_shuffled = random.sample(video_ids_2, len(video_ids_2))
#
# # assign groups for video ids by using odd and even numbers respectively
# groups = {}
# for i, video_id in enumerate(video_ids_1):
#     groups[video_ids[video_id]] = i
#
# for i, video_id in enumerate(video_ids_2_shuffled):
#     groups[video_ids[video_id]] = i
#
# print(groups)
#
# # Create a copy
# train_scaled_groups_df = train_scaled_df.copy()
#
# # Insert group column
# train_scaled_groups_df['group'] = train_scaled_groups_df['video_id'].map(groups)