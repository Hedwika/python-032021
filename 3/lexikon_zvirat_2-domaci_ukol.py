import requests
import pandas as pd

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv")
open("lexikon-zvirat.csv", "wb").write(r.content)

# Načti si soubor pomocí metody read_csv. Pozor, tento dataset využívá jako oddělovač středník, nikoliv čárku.
# Při načítání dat proto nastav parametr sep na znak středníku (";").
lexikon_zvirat = pd.read_csv("lexikon-zvirat.csv", sep=";")

# 1) Poslední sloupec a poslední řádek obsahují nulové hodnoty. Zbav se tohoto sloupce a řádku.
lexikon_zvirat = lexikon_zvirat.iloc[:-1, :-1]

# 2) Nastav sloupec id jako index pomocí metody set_index.
lexikon_zvirat = lexikon_zvirat.set_index('id')

# Chceme ke každému zvířeti vytvořit popisek na tabulku do zoo. Popisek bude využívat sloupců:
# - title (název zvířete)
# - food (typ stravy)
# - food_note (vysvětlující doplněk ke stravě)
# - description (jak zvíře poznáme).
# Napiš funkci popisek, která bude mít jeden parametr radek. Funkce spojí informace dohromady.
# Následně použijte metodu apply, abyste vytvořili nový sloupec s tímto popiskem.

def popisek(radek):
    nazev = str(radek.title)
    strava_uvod = "preferuje následující typ stravy: "
    strava = str(radek.food)
    strava_meziclanek = ". Konkrétně ocení, když mu do misky přistanou "
    strava_podrobne = str(radek.food_note)
    popis_uvod = ". Jak toto zvíře poznáme: "
    popis = str(radek.description)
    return nazev + strava_uvod + strava + strava_meziclanek + strava_podrobne + popis_uvod + popis

lexikon_zvirat["popisek"] = lexikon_zvirat.apply(popisek, axis=1)
print(lexikon_zvirat)