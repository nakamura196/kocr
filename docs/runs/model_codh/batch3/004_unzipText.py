import json
import glob
import os
import gzip

targets = ["lc"] # ["kyushu", "kyushu_m", "nijl_s", "utokyo_l"]

for target in targets:
    files = glob.glob("../output/{}-*/text.json.gzip".format(target))

    for file in sorted(files):
        print(file)

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

    