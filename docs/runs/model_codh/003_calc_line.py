# file_id = "kyushu_42"
# vol = 42
# conf_vol = 42
# attribution = "九州大学"
# target = "kyushu_m"
root = "/content/kocr/docs/runs/model_codh"
root = "."

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id', help='foooo')
parser.add_argument('attribution', help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
# vol= args.vol # "genji_0001"


file_id = args.id

attribution = args.attribution

vol = int(file_id.split("-")[-1])

target = file_id.replace("-" + file_id.split("-")[-1], "")

conf_vol = vol
# file_id = target + "-"+str(vol).zfill(2)

import Levenshtein
import json
import requests

def getLines():
  with open("../../../ndl.json") as f:
      df = json.load(f)

  map = {}

  for obj in df:
      label = obj["label"]
      page = obj["page"]

      map[page] = label

  return map

lines = getLines()



def getTestData():

  testLineArray = []
  # linesMap = {}

  canvas_labels = {}

  path = root + "/output/{}/map.json".format(file_id)
  hash_canvas_map = {}
  canvas_list = []
  with open(path) as f:
    df = json.load(f)
    for obj in df:
      hash_canvas_map[obj["objectID"]] = {
          "canvas": obj["canvas"],
          "label": obj["label"]
          }

      canvas_labels[obj["canvas"]] = obj["label"]

      canvas_list.append(obj["canvas"])

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
    values = df[page][target]

    if len(values) > 0:
      canvases = []
      for value in values:
        canvases.append(hash_canvas_map[value["id"]])
      test[int(page)] = canvases

  return test, canvas_labels, testLineArray, canvas_list

test, canvas_labels, testLineArray, canvas_list = getTestData()

total = 0
correct = 0
correctTop2 = 0

# 1ページあたりの文字数で動的に変更
window = 3

canvas_list = None

def getPreviousCanvas(canvas): # , delimiter="p"
  '''
  spl = canvas.split("/" + delimiter)
  p = int(spl[1])
  next_p = p - 1
  return spl[0] + "/" + delimiter + str(next_p)
  '''
  index = canvas_list.index(canvas)
  
  if index > 0:

    return canvas_list[index - 1]
  else:
      return None

error_top1 = {}
error_topX = {}

def getCanvasIdTop(data):
  if(len(data) == 1):
    return data[0]["canvas"]
  else:
    result = None
    canvases = []
    for obj in data:
      canvases.append(obj["canvas"])

    for i in range(len(canvases) - 1):
      currentCanvas = canvases[i]
      # print("currentCanvas", currentCanvas)
      # スコアが次点のカンバス
      nextCanvas = canvases[i+1]

      # print(getPreviousCanvas(currentCanvas), nextCanvas)

      # 一位のカンバスの前のカンバスが、カンバスの並びの次のアイテムの場合
      if getPreviousCanvas(currentCanvas) == nextCanvas:
        # return currentCanvas
        # continue

        result = nextCanvas

      else:
        return currentCanvas
      
        # result = 


  return result

for page in test:
  # print("page", page, )

  # 類似度の高い先頭トップcanvas
  # canvases = test[page][0:1]

  canvas_id_top = getCanvasIdTop(test[page]) # test[page][0]["canvas"]
  # print("canvas_id_top", canvas_id_top)
  
  
  canvas_id_top_previous = getPreviousCanvas(canvas_id_top)

  # 類似が1位と2位のカンバスを使用する
  canvas_ids_top2 = [canvas_id_top, canvas_id_top_previous]

  '''
  if window > 2:
    canvas_id_top_previous2 = getPreviousCanvas(canvas_id_top_previous)
    canvas_ids_top2.append(canvas_id_top_previous2)
  '''

  # 校異源氏物語の1行目
  # 文字数が少ない場合には、2行目も追加？
  koui_2_lines = "".join(lines[page][0:1])

  # <!-- 計算開始 -->
  scores = {}

  def getLine(labels, i, size):
    line2 = ""
    flg = True
    while flg:
      line2 += labels[i]

      if len(line2) > size:
        flg = False

      if len(labels) - 1 == i:
        flg = False

    return line2

  for canvas_id in canvas_ids_top2:
    if canvas_id not in canvas_labels:
      continue
    labels = canvas_labels[canvas_id]
    for i in range(len(labels) - 1):
      # canvas_lines = labels[i:i+2]
      canvas_lines = labels[i:i+1]

      # line = "".join(canvas_lines)

      # 文字の長さが揃うように修正
      line = getLine(labels, i, len(koui_2_lines))

      # print("文字数 koui", len(koui_2_lines), "九州", len(line))

      ratio = Levenshtein.ratio(koui_2_lines, line)
      scores[canvas_id+"#line=" + str(i+1).zfill(2)] = ratio

  score_sorted = sorted(scores.items(), key=lambda x:x[1], reverse=True)

   # </!-- 計算終了 -->

  line_top = score_sorted[0][0]

  print(line_top)
  
