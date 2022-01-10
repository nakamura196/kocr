# file_id = "kyushu_42"
# vol = 42
# conf_vol = 42
attribution = "九州大学"
target = "kyushu"
root = "/content/kocr/docs/runs/model_codh"
root = "../"

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

import Levenshtein
import json

# id = "kyushu_01"
# koui_path = "/content/kocr/ndl.json"
koui_path = "../../../../ndl.json"

target_path = root + "/output/" + file_id + "/map.json"
# file_id = id

map = {}

def getData(path):
  with open(path) as f:
      df = json.load(f)

  for obj in df:
      id = obj["objectID"]
      text = obj["text"]
      attribution = obj["target"]
      vol = obj["vol"]

      if attribution not in map:
          map[attribution] = {}

      if vol not in map[attribution]:
          map[attribution][vol] = {}

      map[attribution][vol][id] = text

getData(koui_path)
getData(target_path)

################

result = {}

for attribution in map:

    vols = map[attribution]

    # print(attribution)

    if attribution != "校異源氏物語":
        continue

    for vol in vols:

        # print(vol)

        obj = vols[vol]

        for id in obj:

            # print(id)

            result[id] = {}

            text = obj[id]

            for attribution2 in map:
                if attribution == attribution2:
                    continue

                if attribution2 not in result[id]:
                    result[id][attribution2] = {}

                vols2 = map[attribution2]

                for vol2 in vols2:
                    if vol != vol2:
                        continue

                    obj2 = vols2[vol2]

                    for id2 in obj2:
                        
                        text2 = obj2[id2]
                        
                        # ratio = 1 - Levenshtein.distance(text, text2) / max(len(text), len(text2)) * 1.00
                        ratio = Levenshtein.ratio(text, text2)

                        result[id][attribution2][id2] = ratio

        # break

all = {}
all2 = {}

for id in result:
    # print(id, result[id])

    obj3 = result[id]

    map = {}
    all[id] = map

    for attribution in obj3:

        obj = obj3[attribution]

        arr = []

        score_sorted = sorted(obj.items(), key=lambda x:x[1], reverse=True)

        max = 10

        if len(score_sorted) < max:
            max = len(score_sorted)

        for i in range(0, max):

            obj2 = score_sorted[i]

            
            arr.append({
                "id" : obj2[0],
                "score" : obj2[1]
            })
            
            # arr.append(obj2[0])

        map[attribution] = arr

        if len(arr) > 0:
          all2[id] = arr

opath = root + "/output/{}/calc.json".format(file_id)

with open(opath, 'w') as outfile:
    json.dump(all, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))

#####

opath = root + "/output/{}/calc2.json".format(file_id)

with open(opath, 'w') as outfile:
    json.dump(all2, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))