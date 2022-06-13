import glob
import json
import pandas as pd
import requests
import os

path = "../data/bib.json"
path2 = "../data/bib2.json"

df = requests.get("https://script.google.com/macros/s/AKfycbweFcBogWLgf7AyFboBOAnKxqeJr_cVQEk3PPODAEA5KBgr_rywx6IQm8ug5MS-A5F1/exec?sheet=all").json()


map = {}
arr = []

for obj in df:
  sheet = obj["label"]
  if sheet in ["metadata"]:
    values = obj["value"]

    for value in values:
      id = value["id"]
      if id == "":
        continue
      value2 = {}
      for key in value:
        if key[0] != "_":
          value2[key] = value[key]
      map[id] = value2

      arr.append(value2)

with open(path, 'w') as outfile:
    json.dump(map, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))

with open(path2, 'w') as outfile:
    json.dump(arr, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))