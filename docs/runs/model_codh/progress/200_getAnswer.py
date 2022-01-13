import json
import requests

answerAttr = "九大本（古活字版）"

# vols = [2]
vols = []

for i in range(54):
  vols.append(i+1)

print(len(vols))

answerVolMap = {}

for vol in vols:

  print("vol", vol)

  conf_vol = vol

  answers = []

  def getAnswers():
    df = requests.get("https://genji.dl.itc.u-tokyo.ac.jp/data/vol/{}/curation.json".format(str(conf_vol).zfill(2))).json()
    selections = df["selections"]

    for selection in selections:
      if answerAttr in selection["@id"]:
        members = selection["members"]
        for member in members:

          metadata = member["metadata"]
          for m in metadata:
            value = m["value"]
            if "校異源氏物語" not in value:
              continue
            page = int(m["value"].split("p.")[1])

            if page not in answers:
              answers.append(page)

    return answers

  answers = getAnswers()
  answerVolMap[conf_vol] = answers


with open("data.json", 'w') as outfile:
    json.dump(answerVolMap, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))