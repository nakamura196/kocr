set -e

# URL=$1 # https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif-img/167850/full/3000,/0/default.jpg
# ID=$2 # asia

# URL="https://clioapi.hi.u-tokyo.ac.jp/iiif/81/adata/bd1/BD1000-002200/1/manifest"
# ID="BD1000-002200_1"

# URL="https://clioapi.hi.u-tokyo.ac.jp/iiif/81/tdata/imaijikan/01-01_03-21/4/manifest"
# ID="imaijikan"

#!/bin/bash

URL=$1
ID=$2

START=$4
END=$6

if [ -n "$START" ]; then
  START="-s $START"
fi

if [ -n "$END" ]; then
  END="-e $END"
fi

if [ -e output/$ID/text.json ]; then
  echo "すでに結果が存在するため、本処理を終了します。"
  exit 1
fi

if [ -e output/$ID ]; then
  rm -rf output/$ID
fi

mkdir -p output/$ID

echo "detection"
python detection2.py $URL $ID $START $END

echo "classification"
python classification2.py $ID

echo "text"
python text.py $ID