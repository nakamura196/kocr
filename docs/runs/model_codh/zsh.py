import glob
import gzip
import json
import os

files = glob.glob("output/*/*.json")

for file in files:
    print(file)

    opath = file + ".gzip"

    if not os.path.exists(opath):
        
        with open(file) as f:
            df = json.load(f)

        with gzip.open(opath, 'wt') as fp:
            json.dump(df, fp)