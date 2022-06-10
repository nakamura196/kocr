import glob
import json
import pandas as pd

map = {}

files = glob.glob("../item2/*.json")

files = sorted(files)

for file in files:
  page = int(file.split("/")[-1].split(".")[0])

  # print("page", page)

  with open(file) as f:
    df = json.load(f)

  if page == 5:
    import pprint
    pprint.pprint(df)

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