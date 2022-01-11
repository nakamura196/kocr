set -e

VOL=$1
echo $VOL

echo 001
python 001_create_map.py $VOL

echo 002
python 002_1_calc.py $VOL

echo 003
python 003_calc2.py $VOL
