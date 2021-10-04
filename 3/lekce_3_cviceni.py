import requests
import pandas

desired_width = 1000
pandas.set_option('display.width', desired_width)
pandas.set_option('display.max_columns',100)

# Načti si soubor pomocí metody read_csv.
# Pozor, tento dataset využívá jako oddělovač středník, nikoliv čárku.
# Při načítání dat proto nastav parametr sep (jako "separator") na znak středníku (";").
r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/adopce-zvirat.csv")
open("adopce-zvirat.csv", "wb").write(r.content)

adopce_zvirat = pandas.read_csv("adopce-zvirat.csv", sep=";")

# Čištění dat - zbav se řádků a sloupců, které obsahují samé nulové hodnoty.
# Například pro sloupce můžeš využít metody dropna(how='all', axis='columns').
adopce_zvirat = adopce_zvirat.dropna(how="all", axis="columns")
# print(adopce_zvirat.head())

# Chceme adoptovat nějaké modré zvíře (tip: v anglickém názvu má "blue").
# Náš rozpočet je maximálně 2500 korun, a zvíře bychom si chtěli před adopcí prohlédnout.
# Úlohu vyřeš dvěma způsoby (v libovolném pořadí):
# 1) Pomocí metody iterrows nebo itertuples
zvirata_k_adopci = []

for idx, zvire in adopce_zvirat.iterrows():
    if zvire['cena'] < 2500.0 and zvire["k_prohlidce"] == 1.0 and "blue" in zvire["nazev_en"].lower():
        zvirata_k_adopci.append(zvire['nazev_en'])

print("Vhodná zvířata k adopci jsou: ")
for zvire in zvirata_k_adopci:
    print(f"- {zvire}")

# 2) Pomocí dotazu (filtrování dat)
vhodna_zvirata = adopce_zvirat[(adopce_zvirat["k_prohlidce"] == 1.0) & (adopce_zvirat["cena"] < 2500.0) & (adopce_zvirat["nazev_en"].str.contains(r'blue', case=False))]
print(vhodna_zvirata)