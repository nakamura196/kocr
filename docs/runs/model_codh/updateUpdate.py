import glob
import gzip
import json
import os

import json
import gzip

import datetime
import time
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id')
parser.add_argument('attribution')
parser.add_argument('name')
parser.add_argument('user')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
id = args.id # "genji_0001"

spl = id.split("-")
vol = int(spl[-1])
vol_zfill = str(vol).zfill(2)
target = id.replace("-" + vol_zfill, "")

attribution = args.attribution
name = args.name
user = args.user

path = "data/update.json"
with open(path) as f:
  df = json.load(f)

  dt_now = datetime.datetime.now()

  df.append({
    "date": time.time(),
    "user": user,
    "name" : name,
    "attribution" : attribution,
    "vol": vol,
    "id": id
  })

with open(path, 'w') as outfile:
  json.dump(df, outfile, ensure_ascii=False,
  indent=4, sort_keys=True, separators=(',', ': '))

#####

path = "data/status.json"
with open(path) as f:
  df = json.load(f)

  if target not in df:
    df[target] = {}

    for n in range(54):
      df[target][str(n+1).zfill(2)] = 0

  df[target][vol_zfill] = 1

with open(path, 'w') as outfile:
  json.dump(df, outfile, ensure_ascii=False,
  indent=4, sort_keys=True, separators=(',', ': '))

  


