import numpy as np
from src.preprocessing.dataset_creation.helpers import get_fixed_col


def align_audio_video(slices, df_audio):
    filenames_audio = df_audio["filename"]
    filenames_video = get_fixed_col(slices, "filename")

    new_slices = []

    for idx, filename_audio in enumerate(filenames_audio):
        # get index for current filename
        ind = np.where(filenames_video == filename_audio)[0]
        # if not found, skip
        if ind.size == 0:
            print("found filename in audio not in video: ", end="")
            print(filename_audio)
            print("removing")
            df_audio = df_audio.drop(idx, axis=0)
        else:
            # get scalar
            ind = ind[0]
            # push onto slice list
            new_slices.append(slices[ind])

    # check equality
    filenames_audio = df_audio["filename"].values
    filenames_video = get_fixed_col(new_slices, "filename")
    if not np.array_equal(filenames_video, filenames_audio):
        raise Exception("Something went wrong, filename vectors do not align")
    return new_slices, df_audio