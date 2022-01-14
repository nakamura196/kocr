import glob
import json
import pandas as pd

with open("keyPageMap.json") as f:
  map = json.load(f)

with open("volPageMap.json") as f:
  data = json.load(f)

  pageVolMap = {}

  for vol in data:
    for page in data[vol]:
      pageVolMap[page] = vol

map2 = {}

for target in map:
  map2[target] = {}

  for i in range(54):
    map2[target][str(i+1).zfill(2)] = 0

  for page in map[target]:
    vol = pageVolMap[page]
    
    map2[target][str(vol).zfill(2)] = 1

with open("../data/status.json", 'w') as outfile:
  json.dump(map2, outfile, ensure_ascii=False,
  indent=4, sort_keys=True, separators=(',', ': '))