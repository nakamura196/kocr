from dotenv import load_dotenv
load_dotenv()
import os
import shutil

in_dir = "/Users/nakamura/git/genji/kocr"
o_dir = "/Users/nakamura/git/genji/genji-ai"

shutil.copy("{}/docs/runs/model_codh/data/bib.json".format(in_dir), "{}/static/data/bib.json".format(o_dir))
shutil.copy("{}/docs/runs/model_codh/data/bib2.json".format(in_dir), "{}/static/data/bib2.json".format(o_dir))
shutil.copy("{}/docs/runs/model_codh/data/exists.json".format(in_dir), "{}/static/data/exists.json".format(o_dir))

shutil.copy("{}/docs/runs/model_codh/data/status.json".format(in_dir), "{}/static/data/status.json".format(o_dir))
shutil.copy("{}/docs/runs/model_codh/data/update.json".format(in_dir), "{}/static/data/update.json".format(o_dir))

item_dir = "{}/static/data/item".format(o_dir)
shutil.rmtree(item_dir)
shutil.copytree("{}/docs/runs/model_codh/item2".format(in_dir), item_dir)

'''
data_dir = os.environ['data_dir']
app_dir = os.environ['app_dir'] + "/static"

shutil.copy("data/index_static.json", app_dir + "/data/index.json")
shutil.copy("data/docs.json", app_dir + "/data/docs.json")
shutil.copy("data/years.json", app_dir + "/data/years.json")
shutil.copy("data/facets.json", app_dir + "/data/facets.json")
shutil.copy("data/agentials.json", app_dir + "/data/agentials.json")
shutil.copy("data/spatial.json", app_dir + "/data/spatial.json")

# entity関係？

dir = app_dir + "/data/agentials"
shutil.rmtree(dir)
shutil.copytree("data/agentials", dir)

shutil.copy("data/entity.json", app_dir + "/data/entity.json")

api_dir = app_dir + "/api"
date_dir = api_dir+"/date"
if os.path.exists(date_dir):
    shutil.rmtree(date_dir)
shutil.copytree("data/date", date_dir)
'''