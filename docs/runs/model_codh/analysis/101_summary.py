import glob
import json
itemSetId = "kyushu"
files = glob.glob("data/{}/*.json".format(itemSetId))

files = sorted(files)

total = 0
top1 = 0
top2 = 0

for file in files:
  if "error" not in file:
    with open(file) as f:
      df = json.load(f)

      total += df["total"]
      top1 += df["top1"]
      top2 += df["top2"]

window = 3

print("正解Top1", top1, "全体", total, "比率", top1 / total * 100)
print("正解Top{}".format(window), top2, "全体", total, "比率", top2 / total * 100)

      
#########

print("カンバスレベルのマッチングでエラーがあったもの")

for file in files:
  if "error_topX" in file:
    with open(file) as f:
      df = json.load(f)

      vol = file.split("/")[-1].split("_")[0]

      if (len(df) > 0):

        print(vol, len(df))

#########

print("行レベルのマッチングでエラーがあったもの")

for file in files:
  if "error_top1" in file:
    with open(file) as f:
      df = json.load(f)

      vol = file.split("/")[-1].split("_")[0]

      if (len(df) > 0):

        print(vol, len(df))