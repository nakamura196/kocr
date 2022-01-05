set -e

# URL=$1 # https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif-img/167850/full/3000,/0/default.jpg
# ID=$2 # asia

# URL="https://clioapi.hi.u-tokyo.ac.jp/iiif/81/adata/bd1/BD1000-002200/1/manifest"
# ID="BD1000-002200_1"

# URL="https://clioapi.hi.u-tokyo.ac.jp/iiif/81/tdata/imaijikan/01-01_03-21/4/manifest"
# ID="imaijikan"

URL=$1
ID=$2

mkdir -p output/$ID
python detection2.py $URL $ID
python classification2.py $ID