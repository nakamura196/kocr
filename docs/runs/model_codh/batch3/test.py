import json
import glob
import os
import gzip

file = "/Users/nakamurasatoru/git/d_genji/genji-ai/static/data/docs.json"

with open(file) as f:
    df = json.load(f)

files = glob.glob("/Users/nakamurasatoru/git/d_genji/genji-ai/static/data/json/*.json")

map = {}
canvasMap = {}

attrMap = {}

for file in files:
    '''
    if "ndl02" not in file:
        continue
    print(file)
    '''

    with open(file) as f:
        df2 = json.load(f)

    for id in df2:
        item = df2[id]
        map[id] = item
        canvasMap[item["canvas"]] = item

        target = item["target"]
        vol = item["vol"]

        if target not in attrMap:
            attrMap[target] = {}

        if vol not in attrMap[target]:
            attrMap[target][vol] = {}

        attrMap[target][vol][item["page"]] = item

        # print(item["canvas"])

    # print("attrMap", attrMap)

for target in attrMap:

    tmp = attrMap[target]

    canvas_list = []

    for vol in sorted(tmp):

        items = attrMap[target][vol]

        # items = attrMap[target]

        # print(items)

        for page in sorted(items):
            canvas_list.append(items[page]["canvas"])

    attrMap[target] = canvas_list

canvas_list = None

def getPreviousCanvas(canvas):
  # print("canvas_list", canvas_list, "canvas", canvas)
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

for page in df:
    # print("page", page)
    arr = df[page]["arr"]

    for target in arr:

        print("attr", target)

        values = arr[target]
        scores = []

        for value in values:
            scores.append(value["score"])

        
        from statistics import mean
        m = mean(scores)
        # print("平均", m)

        import numpy as np
        np.histogram(scores)


        bins = 100
        hist, bins = np.histogram(scores, bins=bins, range=(scores[-1], scores[0]))

        th_v = (scores[0] + m) / 2

        # print("th_v", th_v)

        values2 = []

        value = values[0]
        if value["score"] > th_v:
            # print(value)
            value["canvas"] = map[value["id"]]["canvas"]
            values2.append(value)

        # print(attrMap[target])

        canvas_list = attrMap[target]

        print("values2", values2)

        canvas_id_top = getCanvasIdTop(values2)

        print("canvas_id_top", canvas_id_top)

        canvas_ids_top2 = [canvas_id_top]

        canvas_id_top_previous = getPreviousCanvas(canvas_id_top)
        if canvas_id_top_previous:

            # 類似が1位と2位のカンバスを使用する
            canvas_ids_top2.append(canvas_id_top_previous)

        #

        arr2 = []

        for canvas_id in canvas_ids_top2:
            if canvas_id in canvasMap:
                obj = canvasMap[canvas_id]
                # print(obj)
                obj2 = {
                    "attribution" : obj["attribution"],
                    "work": obj["work"],
                    "manifest" : obj["manifest"],
                    "canvas" : obj["canvas"],
                    "page" : obj["page"],
                    "type" : obj["type"],
                    "image" : obj["image"]
                }

                arr2.insert(0, obj2)
                # break

        path = "../item/" + page + ".json"

        with open(path) as f:
            df3 = json.load(f)

        related = df3["related"]

        related[target] = arr2

        with open(path, 'w') as outfile:
            json.dump(df3, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))


    # break
