import json
import glob
import os
import gzip

targets = ["lc", "kyushu", "kyushu_m", "nijl_s", "utokyo_l", "ocha", "tsukuba"]

for target in targets:
    files = glob.glob("../output/{}-*/map.json".format(target))

    for file in sorted(files):
        # print(file)

        with open(file, 'r') as f:
            df = json.load(f)

        text = str(df)

        if "ててて" in text:
            print(file)
            

    