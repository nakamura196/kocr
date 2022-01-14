import glob
import json
import pandas as pd
import requests
import os

path = "../data/exists.json"

df = requests.get("https://script.google.com/macros/s/AKfycbweFcBogWLgf7AyFboBOAnKxqeJr_cVQEk3PPODAEA5KBgr_rywx6IQm8ug5MS-A5F1/exec?sheet=all").json()


map = {}

for obj in df:
  sheet = obj["label"]
  if sheet not in ["metadata", "template"]:
    id = sheet
    values = obj["value"]

    # print(id)

    map[id] = {}

    for value in values:
      exists = value["exists"]
      if int(exists) == 0:

        # print(exists)
        map[id][str(value["vol"]).zfill(2)] = -1

with open(path, 'w') as outfile:
    json.dump(map, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))