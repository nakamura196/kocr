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

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('manifest', help='この引数の説明（なくてもよい）')    # 必須の引数を追加
parser.add_argument('id', help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# manifest = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/c1ea8e6b-9403-4394-8619-96aad0ec6329/manifest" # args.url
# item_id = "genji_0001" # args.id

manifest = args.manifest # "https://clioapi.hi.u-tokyo.ac.jp/iiif/81/adata/bd1/BD1000-002200/1/manifest"
item_id = args.id # "BD1000-002200_1"

model = torch.hub.load('ultralytics/yolov5', 'custom', path='../../best.pt') # .autoshape()  # force_reload = recache latest code
model.eval()

df = requests.get(manifest).json()

canvases = df["sequences"][0]["canvases"]

members = []

for c in tqdm(range(len(canvases))):
    canvas = canvases[c]

    canvas_id = canvas["@id"]
    
    url = canvas["images"][0]["resource"]["service"]["@id"] + "/full/1024,/0/default.jpg"
    # print(url)

    tmp_path = "output/{}/detection/{}.jpg".format(item_id, str(c + 1).zfill(4))

    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)

    request.urlretrieve(url, tmp_path)

    img = Image.open(tmp_path)

    width, height = img.size

    results = model(img, size=1024)

    data = results.pandas().xyxy[0].to_json(orient="records")
    data = json.loads(data)

    # print(data)

    r = canvas["width"] / 1024

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
                                    "border-color": "#e41a1c",
                                    "border-width": 1
                                }
                            }
                        }
                    ]
                }
            ],
            "image" : canvas["images"][0]["resource"]["service"]["@id"],
            "thumbnail" : canvas["images"][0]["resource"]["service"]["@id"] + "/" + xywh + "/200,/0/default.jpg",
            "width" : canvas["width"]
        }

        members.append(member)

    # break

    if c > 10: # 3:
        # pass
        break

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