import glob
import gzip
import json
import os

import json
import gzip

root = "."

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id', help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
file_id = args.id # "genji_0001"

vol = int(file_id.split("-")[-1])

target = file_id.replace("-" + file_id.split("-")[-1], "")

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

def getTestData():

  testLineArray = []
  # linesMap = {}

  canvas_labels = {}

  path = root + "/output/{}/map.json".format(file_id)
  hash_canvas_map = {}
  canvas_map = {}

  canvas_list = []

  with open(path) as f:
    df = json.load(f)
    for obj in df:
      hash_canvas_map[obj["objectID"]] = obj
      canvas_map[obj["canvas"]] = obj

      canvas_list.append(obj["canvas"])

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
    values = df[page][target]

    if len(values) > 0:
      canvases = []
      for value in values:
        canvases.append(hash_canvas_map[value["id"]])
      test[int(page)] = canvases

  return test, canvas_labels, testLineArray, canvas_map, canvas_list

test, canvas_labels, testLineArray, canvas_map, canvas_list = getTestData()

path = root + "/output/{}/line.json".format(file_id)
with open(path) as f:
  lineMap = json.load(f)

for page in test:
  # print("page", page)

  page_f = str(page).zfill(4)

  item_path = "item/" + page_f +".json"

  with open(item_path) as f:
    df = json.load(f)

  arr = []
  df["related"][target] = arr

  # 類似度の高い先頭トップcanvas
  # canvases = test[page][0:1]

  canvas_id_top = getCanvasIdTop(test[page])
  canvas_ids_top2 = [canvas_id_top]

  # print("canvas_list", canvas_list)

  # print("canvas_id_top", canvas_id_top)

  canvas_id_top_previous = getPreviousCanvas(canvas_id_top)

  # print("canvas_id_top_previous", canvas_id_top_previous)

  if canvas_id_top_previous:

    # 類似が1位と2位のカンバスを使用する
    canvas_ids_top2.append(canvas_id_top_previous)

  line_id = lineMap[page_f]
  spl = line_id.split("#line=")

  for canvas_id in canvas_ids_top2:
      if canvas_id in canvas_map:
        obj = canvas_map[canvas_id]
        # print(obj)
        obj2 = {
            "attribution" : obj["attribution"],
            "work": obj["work"],
            "manifest" : obj["manifest"],
            "canvas" : obj["canvas"],
            "page" : obj["page"],
            "type" : obj["type"],
            "image" : obj["image"],
            "name" : obj["name"]
        }

        if spl[0] == canvas_id:
          obj2["line"] = spl[1]

        arr.insert(0, obj2)

  with open(item_path, 'w') as outfile:
    json.dump(df, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))

  


