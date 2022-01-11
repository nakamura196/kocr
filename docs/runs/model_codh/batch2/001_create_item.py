import json

koui_path = "../../../../ndl.json"

with open(koui_path) as f:
    df = json.load(f)
    for i in range(len(df)):
        obj = df[i]
        page = str(obj["page"]).zfill(4)

        item_path = "../item/" + page + ".json"

        with open(item_path) as f:
            obj2 = json.load(f)

        try:
            obj2["prev"] = str(df[i - 1]["page"]).zfill(4)
        except:
            pass

        try:
            obj2["next"] = str(df[i + 1]["page"]).zfill(4)
        except:
            pass

        # del obj2["image"]
        # obj2["label"] = obj["label"]

        with open(item_path, 'w') as outfile:
            json.dump(obj2, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))