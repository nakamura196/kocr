import numpy as np
import keras.models
import tensorflow as tf
from PIL import Image
import torch
from urllib import request
import json
import requests
from tqdm import tqdm
import os
import warnings
warnings.filterwarnings("ignore")
import argparse    # 1. argparseをインポート

def getColor(score):
    '''
    if score < 0.1:
        return "#0000FF"
    elif score < 0.2:
        return "#0055FF"
    elif score < 0.3:
        return "#0055FF"
    elif score < 0.4:
        return "#0055FF"
    elif score < 0.5:
        return "#0055FF"
    elif score < 0.6:
        return "#236BFF"
    elif score < 0.7:
        return "#81DCFF"
    elif score < 0.8:
        return "#FFD26F"
    elif score < 0.9:
        return "#FF5500"
    else:
        return "#FF5500"
    '''
    if score < 0.6:
        return "#0000FF"
    elif score < 0.8:
        return "#FF5500"
    else:
        return "#FF0000"

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('manifest', help='この引数の説明（なくてもよい）')    # 必須の引数を追加
parser.add_argument('id', help='foooo')
parser.add_argument('--start', "-s", default=-1, type=int, help='foooo')
parser.add_argument('--end', "-e", default=-1, type=int, help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# manifest = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/c1ea8e6b-9403-4394-8619-96aad0ec6329/manifest" # args.url
# item_id = "genji_0001" # args.id

manifest = args.manifest # "https://clioapi.hi.u-tokyo.ac.jp/iiif/81/adata/bd1/BD1000-002200/1/manifest"
item_id = args.id # "BD1000-002200_1"

# 開始と終了が指定されている場合
s = args.start # "BD1000-002200_1"
e = args.end # "BD1000-002200_1"

if s > -1:
    s = s - 1
    e = e - 1

model = torch.hub.load('ultralytics/yolov5', 'custom', path='../../../best.pt') # .autoshape()  # force_reload = recache latest code
model.eval()

df = requests.get(manifest).json()

canvases = df["sequences"][0]["canvases"]

members = []

image_size = 1024

print("Downloading images && detecting boxes ...")

if s > -1:
    canvases = canvases[s:e+1]

for c in tqdm(range(len(canvases))):

    canvas = canvases[c]

    canvas_id = canvas["@id"]

    c_width = canvas["width"]
    c_height = canvas["height"]
    
    # url = canvas["images"][0]["resource"]["service"]["@id"] + "/full/1024,/0/default.jpg"
    url = canvas["images"][0]["resource"]["@id"]
    # print(url)

    tmp_path = "output/{}/detection/{}.jpg".format(item_id, str(c + 1).zfill(4))

    if not os.path.exists(tmp_path):

        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)

        opener=request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        request.install_opener(opener)
        request.urlretrieve(url, tmp_path)

    img = Image.open(tmp_path)

    w, h = img.size

    # 長い辺
    ll = max(w, h)

    # 1024以下の場合がある
    yolo_input_size = min(image_size, ll)

    # 大きい場合には、小さくする
    if ll > image_size:
        r2 = image_size / ll
        img = img.resize((int(w * r2), int(h * r2)))

    results = model(img, size=yolo_input_size)

    data = results.pandas().xyxy[0].to_json(orient="records")
    data = json.loads(data)

    # ダウンロードした画像がmaxを超える場合がある
    r = max(c_width, c_height) / yolo_input_size

    for i in range(len(data)):
        obj = data[i]

        score = obj["confidence"]

        if score < 0.4:
            pass
            # continue

        index = i + 1

        x = int(obj["xmin"] * r)
        y = int(obj["ymin"] * r)
        w = int(obj["xmax"] * r) - x
        h = int(obj["ymax"] * r) - y

        xywh = "{},{},{},{}".format(x, y, w, h)

        member_id = canvas_id + "#xywh=" + xywh

        index = len(members) + 1

        member = {
            "@id": member_id,
            "@type": "sc:Canvas",
            "label": "[{}]".format(index),
            "metadata": [
                {
                    "label": "Annotation",
                    "value": [
                        {
                            "@id": member_id + "#{}".format(index),
                            "@type": "oa:Annotation",
                            "motivation": "sc:painting",
                            "on": member_id,
                            "resource": {
                                "@type": "cnt:ContentAsText",
                                "chars": "item<br/>{}".format(score),
                                "format": "text/html",
                                "marker": {
                                    "border-color": getColor(score),
                                    "border-width": 1
                                }
                            }
                        }
                    ]
                }
            ],
            "width" : canvas["width"],
            # "height" : canvas["height"]
        }

        members.append(member)

    # break

    if c > 0: # 3:
        pass
        # break

curation = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": "aaa",
    "@type": "cr:Curation",
    "selections": [
        {
            "@id": manifest,
            "@type": "sc:Range",
            "members": members,
            "within": {
                "@id": manifest,
                "@type": "sc:Manifest",
                "label": df["label"]
            }
        }
    ],
    "viewingHint": "annotation"
}

with open("output/{}/curation.json".format(item_id), 'w') as outfile:
    json.dump(curation, outfile) 
    # , ensure_ascii=False,
    #        indent=4, sort_keys=True, separators=(',', ': '))