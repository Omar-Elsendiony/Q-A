import json


with open(r"O:\DriveFiles\\CCE\datasets\\python\data\\python\\jsons\\0.json", "r") as f:
    data = f.read()
    data = json.loads(data)
    firstElement = data[123]

    # print(firstElement[0]["code_tokens"], firstElement[0]["verdict"])


with open(r"O:\DriveFiles\\CCE\datasets\\python\data\\python\\processed_with_verdict\\test.jsonl", "r") as f:
    data = f.read()
    data = json.loads(data)
    firstElement = data[123]

    # print(firstElement)



import pandas as pd

# read
df = pd.read_parquet(r'O:\DriveFiles\\CCE\datasets\defectors\\line_bug_prediction_splits\\time\\test.parquet\\test.parquet')

# write
# df.to_parquet('my_newfile.parquet')

df.head()