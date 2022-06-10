import json

file = "../progress/gas.json"

map = {}

with open(file) as f:
    df = json.load(f)

    arr = df["genji"]

    for item in arr:
        map[item["label"]] = item["value"]

file = "../data/status.json"
with open(file) as f:
    status = json.load(f)

file = "../data/exists.json"
with open(file) as f:
    exists = json.load(f)


values = map["metadata"]

lines = []

for obj in values:
    sheet_id = obj["id"]

    lines.append('''echo '''.format(sheet_id))

    attribution = obj["attribution"]

    name = obj["name"] or sheet_id

    if sheet_id not in map:
        continue

    arr = map[sheet_id]

    print(sheet_id, len(arr))

    for item in arr:
        id = item["id"]
        print(id, attribution, name)

        vol = id.split("-")[1]

        isExists = exists[sheet_id][vol] if (sheet_id in exists and vol in exists[sheet_id]) else 0

        if sheet_id not in status or (status[sheet_id][vol] == 0 and isExists != -1):

            lines.append('''sh 100_batch.sh {} {} {}'''.format(id, attribution, name))

    '''
    values = df["genji"][0]["value"]

    

    for obj in values:
        sheet_id = obj["id"]

        print(sheet_id)
    '''

with open('200_batches.sh', 'w') as f:
    f.write("\n".join(lines))
