import json
import requests
import os
import shutil
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id')
parser.add_argument('password')

args = parser.parse_args()    # 4. 引数を解析

id = args.id
password = args.password

args = parser.parse_args()    # 4. 引数を解析

path = "metadata.json"

if not os.path.exists(path):
  df = requests.get("https://script.google.com/macros/s/AKfycbweFcBogWLgf7AyFboBOAnKxqeJr_cVQEk3PPODAEA5KBgr_rywx6IQm8ug5MS-A5F1/exec?sheet=all").json()
  with open(path, 'w') as outfile:
    json.dump(df, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))

with open(path) as f:
  df = json.load(f)

metadata = None
values = None

for obj in df:
  if obj["label"] == "metadata":
    for obj2 in obj["value"]:
      if obj2["id"] == id:
        metadata = obj2

  if obj["label"] == id:
    values = obj["value"]

# print(metadata)

# print(values)

lines = []
lines.append("set -e")

for value in values:
  if value["start"] == "-1" or value["end"] == "-1":
    continue
  
  value_id = value["id"]

  odir = "output/{}".format(value_id)

  if os.path.exists(odir + "/text.json.gzip"):
    # pass
    continue
  
  # 初期化

  os.makedirs(odir, exist_ok=True)

  start = "-s {}".format(value["start"]) if value["start"] != "" else ""
  end = "-e {}".format(value["end"]) if value["end"] != "" else ""
  # lines.append("sh ocr.sh {} {} {} {}".format(value["manifest"], value_id, start, end))
  
  lines.append("echo '■■■ {}'".format(value_id))
  
  
  lines.append("echo '■■■ detection'")
  lines.append("python detection2.py {} {} {} {}".format(value["manifest"], value_id, start, end))
  
  lines.append("echo '■■■ classification'")
  lines.append("python classification2.py {}".format(value_id))

  lines.append("echo '■■■ text'")
  lines.append("python text.py {}".format(value_id))

  lines.append("echo '■■■ gzip'")
  lines.append("python zsh.py {}".format(value_id))

  lines.append("git pull")


  lines.append("echo '■■■ calc similarity'")

  lines.append("python 001_create_map.py '{}' '{}' '{}'".format(value_id, metadata["attribution"], metadata["name"]))
  lines.append("python 002_calc.py {}".format(value_id))
  lines.append("python 003_calc_line.py {}".format(value_id))
  
  lines.append("python updateUpdate.py '{}' '{}' '{}' '{}'".format(value_id, metadata["attribution"], metadata["name"], metadata["user"]))
  
  lines.append("python updateItem.py {}".format(value_id))
  

  
  lines.append("echo '■■■ git'")
  lines.append("git config --global user.email 'na.kamura.1263@gmail.com'")
  lines.append("git config --global user.name '{}'".format(metadata["user"]))
  lines.append("git remote set-url origin https://nakamura196:{}@github.com/nakamura196/kocr.git".format(password))
  lines.append("git pull")
  


  lines.append("git add /content/kocr/docs/runs/model_codh/output/{}".format(value_id))
  lines.append("git commit /content/kocr/docs/runs/model_codh/item /content/kocr/docs/runs/model_codh/update.json -m 'update item with {} by google colab'".format(value_id))
  lines.append("git commit /content/kocr/docs/runs/model_codh/output/{} -m 'add {} by google colab'".format(value_id, value_id))
  lines.append("git push origin main")
  

with open("main.sh", mode='w') as f:
  f.write("\n".join(lines))
