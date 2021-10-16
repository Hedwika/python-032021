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

# Dataset obsahuje sloupec image_src, který má jako hodnoty odkazy na fotky jednotlivých zvířat.
# Napiš funkci check_url, která bude mít jeden parametr radek. Funkce zkontroluje, jestli je odkaz v pořádku
# podle několika pravidel. K odkazu přistoupíš v těle funkce přes tečkovou notaci: radek.image_src. Zkontroluj následující:
# 1) datový typ je řetězec: isinstance(radek.image_src, str)
# 2) hodnota začíná řetězcem "https://zoopraha.cz/images/": radek.image_src.startswith("https://zoopraha.cz/images/")
# 3) hodnota končí buďto JPG nebo jpg.
# Zvol si jeden ze způsobů procházení tabulky, a na každý řádek zavolej funkci check_url.
# Pro každý řádek s neplatným odkazem vypiš název zvířete (title).

def check_url(radek):
    if not isinstance(radek.image_src, str)\
            or not radek.image_src.startswith("https://zoopraha.cz/images/")\
            or not radek.image_src.lower().endswith('jpg'):
        print(radek.title)

for idx, zvire in lexikon_zvirat.iterrows():
    check_url(zvire)