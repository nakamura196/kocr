import glob
import json
import pandas as pd

map = {}

files = glob.glob("../item/*.json")

for file in files:
  page = int(file.split("/")[-1].split(".")[0])

  with open(file) as f:
    df = json.load(f)

  related = df["related"]

  for key in related:
    if key not in map:
      map[key] = []
    map[key].append(page)

for key in map:
  map[key] = sorted(map[key])

with open("keyPageMap.json", 'w') as outfile:
    json.dump(map, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))