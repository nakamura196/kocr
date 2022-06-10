import requests
import json
from tqdm import tqdm

gas = "https://script.google.com/macros/s/AKfycbypPqjCEaOS8mHhJugIccaJyJWKuZLfO6jd5-7Qh6VPXJWQU7pLwMDOxPMLpDMC3eyv2Q/exec?sheet=all"

df = requests.get(gas).json()

results = {}

for book in tqdm(df):
    gas_url = book["gas_url"]
    id_book = book["id"]
    df_book = requests.get(gas_url).json()
    
    # print(df_book)
    results[id_book] = df_book
    
with open("gas.json", 'w') as outfile:
    json.dump(results, outfile, ensure_ascii=False,
    indent=4, sort_keys=True, separators=(',', ': '))