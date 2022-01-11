import json
import glob
import os
import gzip

targets = ["kyushu", "kyushu_m", "nijl_s", "utokyo_l"]

arr = []

for target in targets:
    files = glob.glob("../output/{}-*".format(target))

    for file in files:
        print(file)

        id = file.split("/")[-1]

        arr.append("python 001_create_map.py {} aaa".format(id))
        arr.append("python 002_calc.py {} aaa".format(id))
        arr.append("python 003_calc_line.py {} aaa".format(id))
        arr.append("python updateItem.py {}".format(id))

with open("../tmp.sh", mode='w') as f:
    f.write("\n".join(arr))

    