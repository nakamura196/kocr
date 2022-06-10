id=$1
attribution=$2
name=$3
cd ../
python 001_create_map.py $id $attribution $name
python 002_calc.py $id
python 003_calc_line.py $id
python updateItem.py $id
cd batch_2022