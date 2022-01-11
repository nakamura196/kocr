import json

koui_path = "../../../../ndl.json"

with open(koui_path) as f:
    df = json.load(f)
    for obj in df:
        page = str(obj["page"]).zfill(4)

        item_path = "../item/" + page + ".json"

        obj2 = {
            "vol_str" : obj["vol_str"],
            "page" : obj["page"],
            "type" : obj["type"],
            "manifest" : obj["manifest"],
            "canvas" : obj["canvas"],
            "related" : {}
        }

        with open(item_path, 'w') as outfile:
            json.dump(obj2, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))