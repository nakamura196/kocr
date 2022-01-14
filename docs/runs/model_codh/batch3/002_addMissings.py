import json
import glob
import os
import gzip

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

    arr.append("echo '{}'".format(target))

    for file in sorted(files):
        # print(file)

        id = file.split("/")[-1]

        arr.append("python 001_create_map.py '{}' '{}' '{}'".format(id, map[target]["attribution"], map[target]["name"]))
        arr.append("python 002_calc.py {}".format(id))
        arr.append("python 003_calc_line.py {}".format(id))
        arr.append("python updateItem.py {}".format(id))

with open("../tmp.sh", mode='w') as f:
    f.write("\n".join(arr))

    