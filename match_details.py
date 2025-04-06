import requests
import time
import json
from config.config import HEADERS

# Načtení ze csv suboru
try:
    with open("json/match_ids.json") as f:
        match_ids = json.load(f)
except Exception as e:
    print(f"Chyba při importování dat z match_ids.json: {str(e)}")

all_matches = []
processed = set()

# Načtení detailů zápasů z API
try:
    for i, match_id in enumerate(match_ids):
        if match_id in processed:
            continue
        processed.add(match_id)
        r = requests.get(
            f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}",
            headers=HEADERS
        )
        time.sleep(1.25)
        
        if r.ok:
            all_matches.append(r.json())
        else:
            print(f"Chyba při získávání informací pro: {match_id}")

except Exception as e:
    print(f"Chyba při získávání detailů ze zápasů: {str(e)}")

# Export detailů do json
try:
    with open("json/all_matches.json", "w",encoding ='utf-8') as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)
    print("Vytvořen soubor all_matches.json")
except Exception as e:
    print(f"Chyba při exportování dat do all_matches.json: {str(e)}")
