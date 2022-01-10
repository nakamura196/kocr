import requests
import json

manifest = "https://kotenseki.nijl.ac.jp/biblio/100018286/manifest"
id = "utokyo_l"

df = requests.get(manifest).json()

canvases = df["sequences"][0]["canvases"]

lines = []

for i in range(len(canvases)):
    index = i + 1
    line = "sh batch2.sh {} page-{}-{} -s {} -e {}".format(manifest, id, str(index).zfill(5), index, index)
    lines.append(line)

with open("batch_{}.sh".format(id), mode='w') as f:
    f.write("\n".join(lines))
