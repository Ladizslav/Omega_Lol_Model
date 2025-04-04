# Základní informace
- Jméno projektu: Machine learning
- Autor: Ladislav Dobiáš
- Datum dokončení: 4.4.2025
- Kontaktní údaje: dobias@spsejecna.cz
- Instituce: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30
- Typ projektu: Školní projekt

---

## Příprava aplikace

1. Stáhněte soubor z Moodlu nebo z GitHubu.
2. Spusťte Visual Studio Code.
3. Otevřete terminál a zadejte příkaz:

    python -m venv venv
    cd ./venv/Scripts
    ./pip.exe install pandas
    ./pip.exe install numpy
    ./pip.exe install pickle
    ./pip.exe install sklearn
    ./pip.exe install sklearn.model

    PS: numpy se stahuje automaticky s pandasem a sklearn se musí určit přímo

---

## Nastavení config

1. Otevřte config.py
2. Opravte **API_KEY**, který se musí generovat jednou za 24 hodin na stránce: **[Riot games developer](https://developer.riotgames.com/)**
2.1. Pokud bude potřeba můj, možná budu muset se příhlásit pomocí mobilu na email na comfirm, protože projekt se odevzdává v neděli nejpozději. 

---

## Jak jsem získal data

League of legends (LOL), je od společnosti Riot games který mají vlastní API na všechny jejich hry (LOL, Teamfight Tactics, Valorant atd.).
Vybral jsem si LOL, protože mě zajímalo, jak to vůbec vypadá a co s tím dokážu.

### Postup získávání dat

1. get_puuid.py
2. get_match_ids.py
3. match_details.py
4. player_stats.py
5. player_format.py

### Postum získávání dat text

1. Získání puuid (originálí id hráče na serveru) díký jménu, hashtagu a regionu hráče (viz. players.json).
2. Pomocí puuid získáme id všech posledních 2000 her hráče. 
PS: Nemusí to vyhledat přesně 2000 her, server má jen omezený počet her od roku 2020, takže to spíš hledá méně.
3. Pomocí id hry se získají detaily hry do jednoho json (~5000 řádků json na 1 hru).
4. Hledání detalů hráče díky puuid z detalů hry a uloží se nefiltrované statistiky hráče.
5. Zformátování statistiky hráče na přípravu strojového učení

### Čas na získání dat

Riot games má omezení na 200 za 2 minuty, proto při získávání to trvalo:

    1. 1 sekundu
    2. ~45 minut
    3. ~45 minut
    4. 5 sekund
    5. 1 sekundu

---

## Spuštění aplikace

### Ve Visual Studio Code
1. Otevřete soubor `main.py`.
2. Spusťte skript stisknutím klávesy `F5` nebo příkazem `Run`.
        
### Přímo ze souboru
1. Otevřete terminál.
2. Navigujte do složky, kde se nachází soubor `main.py`.
3. Spusťte příkaz:

    python main.py

---

## Jak aplikace funguje

Po spuštění aplikace se zobrazí menu s dostupnými příkazy, které můžete použít.
Psát můžete rovnou do konzole a aplikace bude reagovat.

---

## Použité soubory z projektu

Ve složce Used_files jsem použil všechny

README2.md - z Bank system alfy na formát toho README
1_nacteni_dat.py - formát na logickou regresy modelu
