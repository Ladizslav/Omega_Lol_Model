import requests
import csv
import json
from config.config import HEADERS

# Načtení hráčů ze souboru json
try:
    with open('json/players.json', 'r') as f:
        players = json.load(f)['players']
except Exception as e:
    print(f"Chyba při importování dat z player.csv: {str(e)}")

puuids = []


# Procházení všech hráčů v seznamu
try:
    for name, tag, platform in players:

            r = requests.get(
                f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}",
                headers=HEADERS
            )
            if r.status_code == 200:
                data = r.json()
                puuids.append({
                    "Summoner Name": f"{name}#{tag}",
                    "PUUID": data["puuid"],
                    "Platform": platform
                })
            else:
                print(f"Chyba při získávání informací pro: {name}")

except Exception as e:
    print(f"Chyba při procházení hráčů: {str(e)}")


# Export puuid do csv
try:
    if puuids:
        with open("csv/puuids.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=puuids[0].keys())
            writer.writeheader()
            writer.writerows(puuids)
        print("Vytvořen soubor puuids.csv")
except Exception as e:
    print(f"Chyba při exportování dat do puuids.csv: {str(e)}")

