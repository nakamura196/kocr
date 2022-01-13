import glob
import json
import pandas as pd

files = glob.glob("../../item/*.json")

key = "kyushu_m"

predicts = {}

for file in files:
  page = str(int(file.split("/")[-1].split(".")[0]))

  with open(file) as f:
    df = json.load(f)

  values = df["related"][key]

  predicts[page] = {
    "canvases" : [],
    "line" : None
  }

  for value in values:
    predicts[page]["canvases"].append(value["canvas"])

    if "line" in value:
      predicts[page]["line"] = value["canvas"]

with open("data.json") as f:
  answers = json.load(f)

rows = []
rows.append(["vol", "total", "correctCanvas", "correctCanvas %", "correctLine", "correctLine %"])

correct_t = 0
correctLine_t = 0
total_t = 0

for vol in answers:
  # print(vol)
  map = {}

  correct = 0
  correctLine = 0
  total = 0

  for page in answers[vol]:
    answer_canvas = answers[vol][page]

    total += 1

    if answer_canvas in predicts[page]["canvases"]:
      correct += 1

    if answer_canvas == predicts[page]["line"]:
      correctLine += 1

  # print("正解Canvas", correct, "全体", total, "比率", correct / total * 100)
  # print("正解Line", correctLine, "全体", total, "比率", correctLine / total * 100)
  rows.append([vol, total, correct, correct / total * 100, correctLine, correctLine / total * 100])

  correct_t += correct
  correctLine_t += correctLine
  total_t += total

rows.append(["sum", total_t, correct_t, correct_t / total_t * 100, correctLine_t, correctLine_t / total_t * 100])

df = pd.DataFrame(rows)

df.to_csv('data.csv', header=False, index=False)