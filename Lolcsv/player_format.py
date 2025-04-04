import csv

# Načtení nefilrovaných statů
try:
    with open('csv/stats_filterless.csv') as f:
        data = list(csv.DictReader(f))
except Exception as e:
    print(f"Chyba při importování z stats_filterless.csv: {str(e)}")
    exit()

# Vytvoření mapování champion jmen na číselné id
try:
    unique_champions = set()
    for row in data:
        unique_champions.add(row['champion'])
except Exception as e:
    print(f"Chyba při vytvoření mapování: {str(e)}")
    exit()

# Přiřazení číselných id
try:
    champion_ids = {}
    for i, champion_name in enumerate(sorted(unique_champions), start=1):
        champion_ids[champion_name] = i
except Exception as e:
    print(f"Chyba při přiřazení číselných id: {str(e)}")
    exit()

# Příprava nových záhlaví sloupců
try:
    fieldnames = [col for col in data[0].keys() if col != 'champion']
    
    fieldnames = [col for col in fieldnames if col not in ['gold', 'damage', 'kills', 'deaths', 'assists']]
    
    fieldnames.extend([
        'champion_id',
        'gold_per_min',
        'damage_per_min',
        'kda_ratio'
    ])
    
    other_columns = [col for col in data[0].keys() 
                    if col not in ['champion', 'gold', 'damage', 'kills', 'deaths', 'assists'] 
                    and col not in fieldnames]
    fieldnames.extend(other_columns)
except Exception as e:
    print(f"Chyba při přípravě nových záhlaví sloupců: {str(e)}")
    exit()

# Zpracování a transformace dat
try:
    processed_data = []
    for row in data:
        new_row = {}
        
        new_row['champion_id'] = champion_ids[row['champion']]
        
        duration_min = float(row['duration']) / 60
        new_row['gold_per_min'] = round(float(row['gold']) / duration_min, 2)
        
        new_row['damage_per_min'] = round(float(row['damage']) / duration_min, 2)
        
        kills = float(row['kills'])
        deaths = float(row['deaths']) if float(row['deaths']) != 0 else 1  
        assists = float(row['assists'])
        new_row['kda_ratio'] = round((kills + assists) / deaths, 2)
        
        for col in row.keys():
            if col not in ['champion', 'gold', 'damage', 'kills', 'deaths', 'assists']:
                new_row[col] = row[col]
        
        processed_data.append(new_row)
except Exception as e:
    print(f"Chyba při transformaci dat: {str(e)}")
    exit()

# Uložení dat do csv
try:
    with open('csv/data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)
    print("Data byla úspěšně zpracována a uložena do data.csv")
except Exception as e:
    print(f"Chyba při ukládání dat do csv data.csv: {str(e)}")

# Uložení listu jmen postav
try:
    with open('csv/champion_mapping.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['champion_id', 'champion_name'])
        writer.writerows(champion_ids.items())
    print("Mapování championů bylo uloženo do champion_mapping.csv")
except Exception as e:
    print(f"Chyba při ukládání dat do csv champion_mapping.csv: {str(e)}")