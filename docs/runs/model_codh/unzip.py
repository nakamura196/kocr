import glob
import gzip
import json
import os

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id', help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
id = args.id # "genji_0001"

file = "output/{}/text.json.gzip".format(id)

with gzip.open(file, 'r') as f:
    df = json.load(f)

opath = file.replace("text.json.gzip", "json/curation.json")

os.makedirs(os.path.dirname(opath), exist_ok=True)

members = df["selections"][0]["members"]

for member in members:
    del member["width"]
    del member["metadata"][0]["value"][0]["resource"]["chars"]

with open(opath, 'w') as outfile:
    json.dump(df, outfile)