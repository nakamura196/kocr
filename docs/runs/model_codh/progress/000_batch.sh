set -e

# Google SpreadSheetのダウンロード
python 001_download_gas.py

# IDの変更
cd ../batch_2022
python 001_create_item2.py

python 002_create_batches.py

sh 200_batches.sh

cd ../progress

# ../item/*.jsonに基づき、keyPageMap.jsonを作成する
python 201_createKeyPageMap.py

# ステータス
python 202_createStatus.py

# 各シートの存在しないものを取得する
# 存在しない巻を取得する
python 300_createExists.py

# 書誌情報のデータ作成
python 301_createBib.py