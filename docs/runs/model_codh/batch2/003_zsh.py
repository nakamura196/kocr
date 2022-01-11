import json
import glob
import os
import gzip

files = glob.glob("/Users/nakamurasatoru/git/d_hi_letter/yolov5-flask-kunshujo/docs/runs/model_codh/output/*/*.json")

for file in files:
    print(file)
    # os.remove(file)

    opath = file + ".gzip"

    with open(file) as f:
        df = json.load(f)
    
    with gzip.open(opath, 'wt') as fp:
        json.dump(df, fp)