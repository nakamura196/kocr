import glob
import json
import pandas as pd
import requests
import os

with open("gas.json") as f:
    df = json.load(f)

mappings = {}

for sheet in df:
    if "genji" not in sheet:
        continue

    values = df[sheet][0]["value"]

    for value in values:
        mappings[value["_id"]] = value["id"]

path = "../data/exists.json"

df = requests.get("https://script.google.com/macros/s/AKfycbweFcBogWLgf7AyFboBOAnKxqeJr_cVQEk3PPODAEA5KBgr_rywx6IQm8ug5MS-A5F1/exec?sheet=all").json()

from tqdm import tqdm

map = {}

for obj in tqdm(df):
  sheet = obj["label"]
  if sheet not in ["metadata", "template", "bk"]:
    id = sheet

    if id in mappings:
      id = mappings[id]

    values = obj["value"]

    print("シート名", id)

    map[id] = {}

    for value in values:
      
      if "exists" in value:
        exists = value["exists"]
        if int(exists) == 0:
          map[id][str(value["vol"]).zfill(2)] = -1

      if "end" in value:
        end = value["end"]
        if end != "" and int(end) == -1:
          map[id][str(value["vol"]).zfill(2)] = -1

# 手動
lc_map = map["lc_2008427768"]

for key in lc_map:
  lc_map[key] = 10


with open(path, 'w') as outfile:
    json.dump(map, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))