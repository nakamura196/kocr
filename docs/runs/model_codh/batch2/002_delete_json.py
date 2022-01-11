import json
import glob
import os

files = glob.glob("/Users/nakamurasatoru/git/d_hi_letter/yolov5-flask-kunshujo/docs/runs/model_codh/output/*/*.json")

for file in files:
    print(file)
    os.remove(file)
