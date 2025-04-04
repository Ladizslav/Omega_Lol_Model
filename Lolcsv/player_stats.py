import csv
import json

# Načtení puuid ze souboru csv
try:
    with open("csv/puuids.csv", encoding='utf-8') as f:
        puuids = {row['PUUID'] for row in csv.DictReader(f)}
except Exception as e:
    print(f"Chyba při importování dat z puuids.csv: {str(e)}")

# Načtení zápasů ze souboru json
try:
    with open("json/all_matches.json",encoding ='utf-8') as f:
        matches = json.load(f)
except Exception as e:
    print(f"Chyba při importování dat z all_matches.json: {str(e)}")

# Zpracování statistik hráčů
try:
    stats = []
    for match in matches:
        match_duration = match.get('info', {}).get('gameDuration', 0)  
        for player in match.get('info', {}).get('participants', []):
            if player.get('puuid') in puuids:
                items = [player.get(f'item{i}') for i in range(6)]
                stats.append({ 
                    "champion": player.get('championName'),
                    "kills": player.get('kills', 0),
                    "deaths": player.get('deaths', 0),
                    "assists": player.get('assists', 0),
                    "gold": player.get('goldEarned', 0),
                    "damage": player.get('totalDamageDealt', 0),
                    "win": 1 if player.get('win', False) else 0, 
                    "duration": match_duration
                })
except Exception as e:
    print(f"Chyba při získávání statistik ze zápasů:")

# Uložení statistik do csv
try:
    if stats:
        with open("csv/stats_filterless.csv","w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=stats[0].keys())
            writer.writeheader()
            writer.writerows(stats)
        print("Vytvořen soubor stats_filterless.csv")
except Exception as e:
    print(f"Chyba při exportování dat do stats_filterless.csv: {str(e)}")

