import glob
import json
import pandas as pd

def getTargets():
  with open("gas.json") as f:
    gas = json.load(f)

    targets = []

    for key in gas:
      if key != "genji":
        continue

      values = gas[key][0]["value"]

      for value in values:
        targets.append(value["id"])

    return targets

with open("keyPageMap.json") as f:
  keyPageMap = json.load(f)

with open("volPageMap.json") as f:
  data = json.load(f)

  pageVolMap = {}

  for vol in data:
    for page in data[vol]:
      pageVolMap[page] = vol

map2 = {}

targets = getTargets()

print("targets", targets)

for target in keyPageMap:
  if target not in targets:
    continue

  print("target", target)

  map2[target] = {}

  for i in range(54):
    map2[target][str(i+1).zfill(2)] = 0

  for page in keyPageMap[target]:
    vol = pageVolMap[page]
    
    map2[target][str(vol).zfill(2)] = 1

with open("../data/status.json", 'w') as outfile:
  json.dump(map2, outfile, ensure_ascii=False,
  indent=4, sort_keys=True, separators=(',', ': '))