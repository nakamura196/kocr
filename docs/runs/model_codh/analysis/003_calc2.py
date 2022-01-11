# file_id = "kyushu_42"
# vol = 42
# conf_vol = 42
attribution = "九州大学"
target = "kyushu"
root = "/content/kocr/docs/runs/model_codh"
root = "../"

import json
import requests
import Levenshtein
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('vol', type=int, help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
vol= args.vol # "genji_0001"

conf_vol = vol
file_id = "kyushu_"+str(vol).zfill(2)

def getLines():
  with open("../../../../ndl.json") as f:
      df = json.load(f)

  map = {}

  for obj in df:
      label = obj["label"]
      page = obj["page"]

      map[page] = label

  return map

lines = getLines()

def getAnswers():
  df = requests.get("https://genji.dl.itc.u-tokyo.ac.jp/data/vol/{}/curation.json".format(str(conf_vol).zfill(2))).json()
  selections = df["selections"]

  answers = {}

  for selection in selections:
    if "九大本（古活字版）" in selection["@id"]:
      members = selection["members"]
      for member in members:
        canvas_id = member["@id"].split("#xywh=")[0]

        '''
        if canvas_id not in answers:
          answers[canvas_id] = []
        '''

        metadata = member["metadata"]
        for m in metadata:
          page = int(m["value"].split("p.")[1])
          # answers[canvas_id].append(page)

          if page not in answers:
            answers[page] = canvas_id

  return answers

answers = getAnswers()

def getTestData():

  testLineArray = []
  # linesMap = {}

  canvas_labels = {}

  path = root + "/output/{}/map.json".format(file_id)
  hash_canvas_map = {}
  with open(path) as f:
    df = json.load(f)
    for obj in df:
      hash_canvas_map[obj["objectID"]] = {
          "canvas": obj["canvas"],
          "label": obj["label"]
          }

      canvas_labels[obj["canvas"]] = obj["label"]

      labels = obj["label"]

      for i in range(len(labels)):
          line_id = obj["canvas"]+"#line=" + str(i+1).zfill(2)
          testLineArray.append(line_id)
          # linesMap[line_id] = 

  path = root + "/output/{}/calc.json".format(file_id)
  with open(path) as f:
    df = json.load(f)

  test = {}

  for page in df:
    values = df[page]["kyushu"]

    if len(values) > 0:
      canvases = []
      for value in values:
        canvases.append(hash_canvas_map[value["id"]])
      test[int(page)] = canvases

  return test, canvas_labels, testLineArray

test, canvas_labels, testLineArray = getTestData()

total = 0
correct = 0
correctTop2 = 0

# 1ページあたりの文字数で動的に変更
window = 3

def getNextCanvas(canvas):
  spl = canvas.split("/p")
  p = int(spl[1])
  next_p = p + 1
  return spl[0] + "/p" + str(next_p)

def getPreviousCanvas(canvas):
  spl = canvas.split("/p")
  p = int(spl[1])
  next_p = p - 1
  return spl[0] + "/p" + str(next_p)

error_top1 = {}
error_topX = {}

for page in test:
  # print("page", page, )

  # 類似度の高い先頭トップcanvas
  # canvases = test[page][0:1]

  canvas_id_top = test[page][0]["canvas"]
  # print("canvas_id_top", canvas_id_top)
  canvas_id_top_previous = getPreviousCanvas(canvas_id_top)
  canvas_ids_top2 = [canvas_id_top, canvas_id_top_previous]

  if window > 2:
    canvas_id_top_previous2 = getPreviousCanvas(canvas_id_top_previous)
    canvas_ids_top2.append(canvas_id_top_previous2)

  # 校異源氏物語の1行目
  # 文字数が少ない場合には、2行目も追加？
  koui_2_lines = "".join(lines[page][0:1])

  # <!-- 計算開始 -->
  scores = {}

  for canvas_id in canvas_ids_top2:
    if canvas_id not in canvas_labels:
      continue
    labels = canvas_labels[canvas_id]
    for i in range(len(labels) - 1):
      canvas_lines = labels[i:i+2]

      line = "".join(canvas_lines)

      ratio = Levenshtein.ratio(koui_2_lines, line)
      scores[canvas_id+"#line=" + str(i+1).zfill(2)] = ratio

  score_sorted = sorted(scores.items(), key=lambda x:x[1], reverse=True)

   # </!-- 計算終了 -->

  line_top = score_sorted[0][0]

  print("line_top", line_top)
  print("line_prev", testLineArray[testLineArray.index(line_top) - 1])
  print("---")

  canvas_id_top = line_top.split("#line=")[0]
  canvas_id_to_by_prev_line = testLineArray[testLineArray.index(line_top) - 1].split("#line=")[0]

  predictCanvases = [canvas_id_top, canvas_id_to_by_prev_line]

  answer_canvas = answers[page]

  total += 1

  if answer_canvas in canvas_ids_top2:
    correctTop2 += 1
  else:
      error_topX[page] = {
          "answer_canvas" : answer_canvas,
          "originalCanvasesTop3" : test[page][0:3],
          "canvas_ids_topX": canvas_ids_top2
      }

  if answer_canvas in predictCanvases:
    correct += 1
  else:
      error_top1[page] = {
          "koui_lines": koui_2_lines,
          "scores_top5" : score_sorted[0:5],
          "answer_canvas" : answer_canvas,
          "canvas_ids_topX": predictCanvases
      }

  
  # print("正解", answer_canvas, )
  # print("Top {}".format(window), canvas_ids_top2)
  

  # print("----")

obj = {
    "total": total,
    "top1" : correct,
    "top2" : correctTop2
}

opath = "data/{}/{}.json".format(target, str(vol).zfill(2))

import os

os.makedirs(os.path.dirname(opath), exist_ok=True)

with open(opath, 'w') as outfile:
    json.dump(obj, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))

with open(opath.replace(".json", "_error_top1.json"), 'w') as outfile:
    json.dump(error_top1, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))

with open(opath.replace(".json", "_error_topX.json"), 'w') as outfile:
    json.dump(error_topX, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))

# print("正解Top1", correct, "全体", total, "比率", correct / total * 100)
# print("正解Top{}".format(window), correctTop2, "全体", total, "比率", correctTop2 / total * 100)