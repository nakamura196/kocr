import numpy as np
import keras.models
import tensorflow as tf
from PIL import Image
import codecs
import json
from tqdm import tqdm
import os
import requests
from urllib import request
import argparse    # 1. argparseをインポート
import pandas as pd
from tqdm import tqdm

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id', help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
id = args.id # "genji_0001"

path = "output/{}/character.json".format(id)

json_open = open(path, 'r')
curation = json.load(json_open)

canvases = {}

indexes = {}

members = curation["selections"][0]["members"]

for i in range(len(members)):
    member = members[i]
    member_id = member["@id"]
    spl = member_id.split("#xywh=")
    canvas = spl[0]
    xywh = spl[1].split(",")

    if canvas not in canvases:

        canvases[canvas] = {
            "width" : member["width"],
            "values" : []
        }

    try:
        canvases[canvas]["values"].append({
            "aid": member["metadata"][0]["value"][0]["@id"],
            # "index" : i,
            "x" : int(xywh[0]),
            "y" : int(xywh[1]),
            "width" : int(xywh[2]),
            "height" : int(xywh[3]),
            "text" : member["metadata"][0]["value"][0]["resource"]["marker"]["text"]
        })

        indexes[member["metadata"][0]["value"][0]["@id"]] = i

    except Exception as e:
        print(e)
        pass

print("Setting reading orders ...")
for canvas in tqdm(canvases):

    boxes = canvases[canvas]["values"]

    width = canvases[canvas]["width"]

    hist = []

    for i in range(width + 1):
        hist.append(0)

    for box in boxes:
        x = box["x"]
        y = box["y"]
        w = box["width"]
        h = box["height"]
        for i in range(x, x+w+1):
            hist[i] += 1

    min = 1000
    max = 0

    for v in hist:
        if min > v:
            min = v
        if max < v:
            max = v

    www2 = 10000000

    # divs = {}
    ids_best = None

    for div in [2, 4, 6, 8 , 10, 12, 14, 16]:

        mean = (max + min) / div

        ############

        isLine = False

        lines = []

        line = {
            "x" : 0
        }

        for x in range(len(hist)):
            v = hist[x]

            # 下に転じる
            if v < mean and isLine:
                isLine = False

                line = {
                    "x" : x
                }

            # 上に転じる
            elif v > mean and not isLine:
                isLine = True

                line["x2"] = x
                lines.append(line)

        if not isLine:
            line["x2"] = width
            lines.append(line)

        ##############

        lines2 = []

        dones = []

        for line in lines:
            center = (line["x"] + line["x2"]) / 2

            line2 = {}

            for box in boxes:
                aid = box["aid"]
                x = box["x"]
                y = box["y"]
                w = box["width"]

                box_center = x + w / 2

                if box_center < center and aid not in dones:
                    if y not in line2:
                        line2[y] = []
                    line2[y].append(box)
                    dones.append(aid)

            if len(line2) > 0:

                lines2.append(line2)

        ##############

        ids = []

        for x in range(len(lines2)):
            line = lines2[len(lines2) - x - 1]

            ids2 = []

            for y in sorted(line):
                values = line[y]
                for v in values:

                    ids2.append(v["aid"])

            ids.append(ids2)

        ## id の並び

        www = 0

        # print(ids)

        for i in range(len(ids)):
            ids2 = ids[i]

            for j in range(len(ids2)):
                id = ids2[j]

                if j != 0:
                    member_b = members[indexes[ids2[j-1]]]
                    member = members[indexes[id]]
                    
                    x_b = int(member_b["@id"].split("#xywh=")[1].split(",")[0])
                    x = int(member["@id"].split("#xywh=")[1].split(",")[0])

                    www += abs(x - x_b)

        # 前より小さくなれば
        if www < www2:
            www2 = www
            ids_best = ids
            
        else:
            pass
            # break

    ids = ids_best 

    for i in range(len(ids)):
        ids2 = ids[i]
        for j in range(len(ids2)):
            id = ids2[j]
            member = members[indexes[id]]
            # 先頭かつ次の行がある
            if j == 0 and i != 0:
                
                member["metadata"][0]["value"][0]["resource"]["marker"]["prev_line"] = ids[i-1][0]

            if j == 0 and i != len(ids) - 1:
                member["metadata"][0]["value"][0]["resource"]["marker"]["next_line"] = ids[i+1][0]
    
            if j != 0:
                member["metadata"][0]["value"][0]["resource"]["marker"]["prev"] = ids2[j - 1]

            if j != len(ids2) - 1:
                member["metadata"][0]["value"][0]["resource"]["marker"]["next"] = ids2[j + 1]

with open(path.replace("character.json", "text.json"), 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))

    