import json
import glob
import os
import gzip
import shutil

targets = ["kyushu"]

for target in targets:

    files = glob.glob("../output/" + target + "_*")

    

    for file in files:
        if "kyushu_m" in file:
            continue
        print(file)

        shutil.copytree(file, file.replace("kyushu_", "kyushu-"))
