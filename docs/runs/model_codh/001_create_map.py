# file_id = "kyushu_42"
# vol = 42
# conf_vol = 42
# attribution = "九州大学"
# target = "kyushu"
root = "/content/kocr/docs/runs/model_codh"
root = "."

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id')
parser.add_argument('attribution')
parser.add_argument('name')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id

file_id = args.id

attribution = args.attribution

name = args.name

vol = int(file_id.split("-")[-1])

target = file_id.replace("-" + file_id.split("-")[-1], "")

# vol= args.vol # "genji_0001"

conf_vol = vol
# file_id = "kyushu_"+str(vol).zfill(2)

import json
import requests
import hashlib

def getConfigMap():
  config = requests.get("https://genji.dl.itc.u-tokyo.ac.jp/data/info.json").json()

  selections = config["selections"]

  config_map = {}

  for selection in selections:
      members = selection["members"]

      for member in members:
          label = member["label"]

          for m in member["metadata"]:
              if m["label"] == "vol":
                  config_map[m["value"]] = label

  return config_map



config_map = getConfigMap()
# print(config_map)

######

def getKoui():
  koui_url = "https://genji.dl.itc.u-tokyo.ac.jp/data/vol/"+str(vol).zfill(2)+"/curation.json"
  k = requests.get(koui_url).json()

  koui = {}

  selections = k["selections"]

  for selection in selections:
      for member in selection["members"]:
          member_id = member["@id"]
          labels = member["label"].split(" ")
          if labels[0] == "校異源氏物語":
              koui[member_id] = labels[1].split("p.")[1].zfill(4)
  return koui

koui = getKoui()
# print(koui)

######

def getManifestData(manifest):
  pages = {}
  m_data = requests.get(manifest).json()

  canvases = m_data["sequences"][0]["canvases"]

  images = {}

  for i in range(len(canvases)):
      page = i+1
      canvas = canvases[i]
      canvas_id = canvas["@id"]

      if "thumbnail" in canvas:
          images[canvas_id] = canvas["thumbnail"]["@id"]
      else:
          images[canvas_id] = canvas["images"][0]["resource"]["service"]["@id"] + "/full/200,/0/default.jpg"

      pages[canvas_id] = page

  return pages, images

def getCanvasTextMap(members):
  # canvas毎のテキストを取得
  member_map = {}
  canvas_map = {}
  for member in members:
    member_id = member["@id"]

    anno_id = member["metadata"][0]["value"][0]["@id"]

    marker = member["metadata"][0]["value"][0]["resource"]["marker"]
    marker["@id"] = anno_id

    member_map[anno_id] = marker # member

    member_id_spl = member_id.split("#xywh=")
    canvas_id = member_id_spl[0]

    if canvas_id not in canvas_map:
      canvas_map[canvas_id] = []
    canvas_map[canvas_id].append(member)

  canvas_text_map = {}

  for canvas_id in canvas_map:
    # 最初のノードを取得する
    start_node_id = None

    for member in canvas_map[canvas_id]:
      marker = member["metadata"][0]["value"][0]["resource"]["marker"]

      if "prev_line" not in marker and "next_line" in marker:
        start_node_id = marker["@id"]
        break

    # print(start_node_id)

    if not start_node_id:
        continue
    
    # IIIFキュレーションリストを再起的に処理する
    data = [""]
    def handle(node_id, line_index):
      node = member_map[node_id]
      data[line_index] += node["text"]

      if "next" in node:
        handle(node["next"], line_index)

      if "next_line" in node:
        data.append("")
        line_index += 1
        handle(node["next_line"], line_index)

    handle(start_node_id, 0)

    canvas_text_map[canvas_id] = data

  return canvas_text_map

import json
import gzip

path = root + "/output/{}/text.json.gzip".format(file_id)
with gzip.open(path, 'r') as f:
  df = json.load(f)

selections = df["selections"]

output = []

for selection in selections:
  members = selection["members"]
  manifest = selection["within"]["@id"]
  pages, images = getManifestData(manifest)
  label = selection["within"]["label"]

  ######

  canvas_text_map = getCanvasTextMap(members)

  #####
  
  map = {}

  index = 1

  for member in members:

      member_id = member["@id"]

      member_id_spl = member_id.split("#xywh=")

      canvasId = member_id_spl[0]

      # 要検討
      if canvasId not in canvas_text_map:
          continue

      page = pages[canvasId]
      
      hash = hashlib.md5(canvasId.encode('utf-8')).hexdigest()

      if canvasId not in map:
          map[canvasId] = {
              "objectID" : hash,
              "attribution" : attribution,
              "target" : target,
              "vol_str" : '{} {}'.format(str(vol).zfill(2), config_map[vol]),
              "vol" : vol,
              "label": canvas_text_map[canvasId],
              "image" : images[canvasId],
              "work" : label,
              "page" : page,
              "pos" : index,
              # "curation" : curationUrl,
              "manifest" : manifest,
              "canvas" : canvasId,
              "koui" : [],
              "type" : "コマ",
              "text": "\n".join(canvas_text_map[canvasId]),
              "name": name
          }

          index += 1

      if member_id in koui:
          map[canvasId]["koui"].append(koui[member_id])

  for canvas in map:
      obj = map[canvas]
      output.append(obj)

opath = root + "/output/" + file_id + "/map.json"

with open(opath, 'w') as outfile:
    json.dump(output, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))