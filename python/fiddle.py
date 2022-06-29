import pandas as pd
import sys
from helpers import get_csv_paths


import hashlib


OPENFACE_PROCESSED="/home/tim/work/su-thesis-project/projects/video_analysis/files/openface/"

paths = get_csv_paths(OPENFACE_PROCESSED)

for path in paths:
    df = pd.read_csv(path)
    break


print(df["filename"])

print(df["frame"])

print(int.from_bytes(hashlib.sha256(b"H").digest()[:4], 'little')) # 32-bit int



hash32 = hash("hej") & 0xffffffff

print(hash32)

