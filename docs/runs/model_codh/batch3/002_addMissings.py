import json
import glob
import os
import gzip
import datetime
import pathlib

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('--date', "-d", default=None)

args = parser.parse_args()    # 4. 引数を解析

date = args.date

file = "../data/bib.json"

with open(file) as f:
    df = json.load(f)

map = {}
for id in df:
    obj = df[id]
    map[id] = {
        "name" : obj["name"],
        "attribution" : obj["attribution"]
    }

arr = []

for target in df:
    files = glob.glob("../output/{}-*".format(target))

    arr.append("echo ' - {}'".format(target))

    for file in sorted(files):

        if date:
            # print(file)
            p = pathlib.Path(file)
            dt = datetime.datetime.fromtimestamp(p.stat().st_ctime)

            dt = dt.split(" ")[0]

            if dt < date:
                continue

        id = file.split("/")[-1]
        
        arr.append("echo ' -- {}'".format(id))
        arr.append("python 001_create_map.py '{}' '{}' '{}'".format(id, map[target]["attribution"], map[target]["name"]))
        arr.append("python 002_calc.py {}".format(id))
        arr.append("python 003_calc_line.py {}".format(id))
        arr.append("python updateItem.py {}".format(id))

with open("../tmp.sh", mode='w') as f:
    f.write("\n".join(arr))

    