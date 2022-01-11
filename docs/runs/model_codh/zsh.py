import glob
import gzip
import json
import os

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id', help='foooo')

args = parser.parse_args()    # 4. 引数を解析

# url = args.url
# id = "BD1000-002200_1" # args.id
id = args.id # "genji_0001"

files = glob.glob("output/{}/*.json".format(id))

for file in files:
    print(file)

    opath = file + ".gzip"

    if not os.path.exists(opath):
        
        with open(file) as f:
            df = json.load(f)

        with gzip.open(opath, 'wt') as fp:
            json.dump(df, fp)