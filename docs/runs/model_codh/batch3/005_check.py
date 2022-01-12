import json
import glob
import os
import gzip
import shutil

targets = ["lc", "kyushu", "kyushu_m", "nijl_s", "utokyo_l", "ocha", "tsukuba"]

for target in targets:
    files = glob.glob("../output/{}-*/map.json".format(target))

    for file in sorted(files):
        # print(file)

        with open(file, 'r') as f:
            df = json.load(f)

        text = str(df)

        if "ししし" in text:
            # print(file)

            path = os.path.dirname(file)
            print(path)

            # shutil.rmtree(path)


    