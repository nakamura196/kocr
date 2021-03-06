import numpy as np
import keras.models
import tensorflow as tf
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import codecs
import json
from tqdm import tqdm
import os
import requests
from urllib import request
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id', help='foooo')
parser.add_argument('--start', "-s", default=-1, type=int, help='foooo')
parser.add_argument('--end', "-e", default=-1, type=int, help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
id = args.id # "genji_0001"

# 開始と終了が指定されている場合
s = args.start # "BD1000-002200_1"
e = args.end # "BD1000-002200_1"

if s > -1:
    s = s - 1
    e = e - 1

imsize = (64, 64)

json_open = open("model/labels.json", 'r')
labels = json.load(json_open)

model = keras.models.load_model("model/model.h5")

def load_image(img, xywh, r = 1):
    x = int(int(xywh[0]) * r)
    y = int(int(xywh[1]) * r)
    w = int(int(xywh[2]) * r)
    h = int(int(xywh[3]) * r)
    im_crop = img.crop((x, y, x+w, y+h))

    img = im_crop.convert('RGB')
    # 学習時に、(64, 64, 3)で学習したので、画像の縦・横は今回 変数imsizeの(64, 64)にリサイズします。
    img = img.resize(imsize)

    # 画像データをnumpy配列の形式に変更
    img = np.asarray(img)
    img = img / 255.0
    return img, im_crop.resize(imsize), x, y

def predict(img):
    prd = model.predict(np.array([img]))

    prelabel = np.argmax(prd, axis=1)[0]
    code = labels[prelabel].replace("U+", "\\u")
    s_from_s_codecs_top = codecs.decode(code, 'unicode-escape')

    value = "{} {} ".format(s_from_s_codecs_top, round(prd[0][prelabel] * 100, 2))

    n = 5
    y_preds = np.argsort(prd, axis=1)[:, -n:]

    prelabels = y_preds[0]

    values = []

    for prelabel in prelabels:
        code = labels[prelabel].replace("U+", "\\u")
        s_from_s_codecs = codecs.decode(code, 'unicode-escape')

        values.append("{} {}".format(s_from_s_codecs, round(prd[0][prelabel] * 100, 2)))

    return {
        "detail" : value + " - " + ", ".join(values), # ""
        "marker" : s_from_s_codecs_top
    }


json_open = open("output/{}/curation.json".format(id), 'r')
curation = json.load(json_open)

manifest = curation["selections"][0]["within"]["@id"]

canvas_list = []

m = requests.get(manifest).json()
canvases = m["sequences"][0]["canvases"]

for c in canvases:
    canvas_list.append(c["@id"])

if s > -1:
    canvas_list = canvas_list[s:e+1]

canvases = {}

for member in curation["selections"][0]["members"]:
    member_id = member["@id"]
    spl = member_id.split("#xywh=")
    canvas = spl[0]
    xywh = spl[1].split(",")

    if canvas not in canvases:
        canvases[canvas] = {
            # "image" : member["image"],
            "width" : member["width"],
            "map" : []
        }

    canvases[canvas]["map"].append(member_id)

result = {}

index = 0

print("Classifying words ...")
for c in tqdm(range(len(canvas_list))):
    canvas = canvas_list[c]

    page = c + 1
    
    # detectionされなかったページ
    if canvas not in canvases:
        continue

    obj = canvases[canvas]

    r_size = obj["width"]

    tmp_path = "output/{}/detection/{}.jpg".format(id, str(page).zfill(4))

    '''
    if not os.path.exists(tmp_path):
        continue
    '''
    
    base_img = Image.open(tmp_path)

    w, h = base_img.size

    r = w / obj["width"]

    for member_id in obj["map"]:
        index += 1
        
        xywh_str = member_id.split("=")[1]

        xywh = xywh_str.split(",")
        img_crop, im, x, y = load_image(base_img, xywh, r)

        p = predict(img_crop)
        result[member_id]  = p

        basename = "{}-{}-{}-{}.jpg".format(str(page).zfill(4), p["marker"] + "_" + str(index).zfill(5), str(w-x).zfill(5), str(y).zfill(5))
        t_path = "output/{}/chars/{}".format(id, basename)
        os.makedirs(os.path.dirname(t_path), exist_ok=True)
        im.save(t_path)

for member in curation["selections"][0]["members"]:
    member_id = member["@id"]

    if member_id in result:
        label = result[member_id]

        member["metadata"][0]["value"][0]["resource"]["chars"] += "<br/>" + label["detail"]
        member["metadata"][0]["value"][0]["resource"]["marker"] = {
            "text" : label["marker"]
        }


with open("output/{}/character.json".format(id), 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
            indent=4, sort_keys=True, separators=(',', ': '))