import json


# with open(r"O:/DriveFiles/CCE/datasets/python/data/python/jsons/0.json", "r") as f:
#     data = f.read()
#     data = json.loads(data)
#     firstElement = data[123]

#     # print(firstElement[0]["code_tokens"], firstElement[0]["verdict"])


# with open(r"D:/DriveFiles/GP/datasets/defectors/line_bug_prediction_splits/time/test.parquet/test.parquet", "r") as f:
#     data = f.read()
    # data = json.loads(data)
    # firstElement = data[123]

    # print(firstElement)




import pandas as pd

# read
# df = pd.read_parquet('D:/DriveFiles/GP/datasets/defectors/line_bug_prediction_splits/time/train.parquet/train.parquet')

# write
# df.to_parquet('my_newfile.parquet')

# df.head()

import gzip
print("Reading the file")

# with open("D:/DriveFiles/GP/defectors/line_bug_prediction_splits/time/test.parquet.gzip", "rb") as f:
#     data = f.read()
#     # print(data)
#     print("Decompressing the file")
#     data = gzip.decompress(data)
#     print("Decompressed")
    # data = gzip.decompress("D:/DriveFiles/GP/defectors/line_bug_prediction_splits/time/test.parquet.gzip")
import magic

r = magic.from_file('D:/DriveFiles/GP/defectors/line_bug_prediction_splits/time/test.parquet.gzip', mime=True)
print(r) # 'application/gzip'