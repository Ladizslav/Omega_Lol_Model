import requests
import csv
import time
import json
from config.config import HEADERS

# Načtení puuid ze csv suboru
try:
    with open("csv/puuids.csv") as f:
        puuids = [row['PUUID'] for row in csv.DictReader(f)]
except Exception as e:
    print(f"Chyba při importování dat z puuids.csv: {str(e)}")

# Získání id her pomocí puuid
try:
    all_match_ids = [
        match_id for puuid in puuids
        for start in range(0, 1000, 100)
        for match_id in requests.get(
            f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids",
            params={'start': start, 'count': 100},
            headers=HEADERS
        ).json()
        if time.sleep(1.25) is None
    ]
except Exception as e:
    print(f"Chyba při získávání id her: {str(e)}")

# Export id her do json
try:
    with open("json/match_ids.json", "w") as f:
        json.dump(all_match_ids, f)
except Exception as e:
    print(f"Chyba při exportování dat do match_ids.json: {str(e)}")
finally:
    print("Vytvořen soubor match_ids.json")

# Odstranění duplicit v match_ids.json
try:
    unique_match_ids = list(dict.fromkeys(all_match_ids))
    with open("json/match_ids.json", "w") as f: 
        json.dump(unique_match_ids, f)
    print("Odstranění duplicit ze souboru match_ids.json")
except Exception as e:
    print(f"Chyba při odstraňování duplicit z match_ids.json: {str(e)}")

