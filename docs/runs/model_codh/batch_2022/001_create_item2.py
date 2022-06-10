import json
import glob
import os
import gzip
import datetime
import pathlib
from tqdm import tqdm
import argparse    # 1. argparseをインポート
import pprint

with open("../progress/gas.json") as f:
    df = json.load(f)

mappings = {}

for sheet in df:
    if "genji" not in sheet:
        continue

    values = df[sheet][0]["value"]

    for value in values:
        mappings[value["_id"]] = value["id"]

pprint.pprint(mappings)


def convert(id):
    if id in mappings:
        return mappings[id]
    return id

files = glob.glob("../item/*.json")

files = sorted(files)

for file in tqdm(files):
    with open(file) as f:
        df = json.load(f)

    related = df["related"]
    related2 = {}

    for id in related:
        id2 = convert(id)
        related2[id2] = related[id]

        # if id != id2:
            
        # del related[id]

    related3 = {}

    for id in sorted(related2):
        related3[id] = related2[id]

    df["related"] = related3

    if "0005" in file:
        pprint.pprint(list(related2.keys()))
        pprint.pprint(len(related2))

    opath = file.replace("/item/", "/item2/")
    os.makedirs(os.path.dirname(opath), exist_ok=True)
    with open(opath, 'w') as f:
        json.dump(df, f, ensure_ascii=False,
                  indent=4, sort_keys=True, separators=(',', ': '))

'''
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
'''