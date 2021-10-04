import matplotlib.pyplot as plt
import pandas
import requests
import math

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/dopravni-urazy.csv")
open("dopravni-urazy.csv", "wb").write(r.content)

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/kraje.csv")
open("kraje.csv", "wb").write(r.content)

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/sportoviste.json")
open("sportoviste.json", "wb").write(r.content)

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/adopce-zvirat.csv")
open("adopce-zvirat.csv", "wb").write(r.content)

urazy = pandas.read_csv("dopravni-urazy.csv")
# print(urazy.head())

kraje = pandas.read_csv("kraje.csv")
print(kraje.head())

urazy_prumer = pandas.DataFrame(columns=["nazev_kraje", "hodnota"])
# print(urazy_prumer)

# Spojime data o krajich s daty o urazech.
# 1. zpusob:
# for idx, kraj in kraje.iterrows():
#     kod_kraje = kraj["kod_polozky"]
#     nazev_kraje = kraj["nazev_polozky"]
#     prumerna_hodnota = urazy[urazy["kraj"] == kod_kraje]["hodnota"].mean()
#     urazy_prumer = urazy_prumer.append({"nazev_kraje": nazev_kraje, "hodnota": prumerna_hodnota}, ignore_index=True)

# print(urazy_prumer)
#
# urazy_prumer.sort_values(by="hodnota").plot.bar(x="nazev_kraje", y="hodnota")
# plt.show()
# 
# 2. zpusob:
# for kraj in kraje.itertuples():
#     kod_kraje = kraj.kod_polozky
#     nazev_kraje = kraj.nazev_polozky
#     prumerna_hodnota = urazy[urazy["kraj"] == kod_kraje]["hodnota"].mean()
#     urazy_prumer = urazy_prumer.append({"nazev_kraje": nazev_kraje, "hodnota": prumerna_hodnota}, ignore_index=True)
#
# print(urazy_prumer)
#
# urazy_prumer.sort_values(by="hodnota").plot.bar(x="nazev_kraje", y="hodnota")
# plt.show()

# 3. zpusob:
# urazy_s_kraji = urazy.merge(kraje, left_on="kraj", right_on="kod_polozky")
# print(urazy_s_kraji.head())
# urazy_s_kraji.groupby("nazev_polozky")["hodnota"].mean().sort_values().plot.bar(x="nazev_polozky", y="hotnota")
# plt.show()

# Vzdálenost od určitého bodu:
sportoviste = pandas.read_json("sportoviste.json")
sportoviste = sportoviste.dropna(how="all", axis="columns")
sportoviste = sportoviste.set_index("OBJECTID")
sportoviste = sportoviste.rename(columns={"POINT_Y": "zemepisna_sirka", "POINT_X": "zemepisna_delka"})

def vzdalenost_od_bodu(radek, bod):
    # Vypocet vzdalenosti mezi dvema body (Eukleidovska vzdalenost)
    vzdalenost = math.sqrt((bod[0] - radek.zemepisna_sirka) ** 2 + (bod[1] - radek.zemepisna_delka) ** 2)
    # Prevod na vzdalenost v kilometrech a zaokrouhleni
    vzdalenost_km = vzdalenost * (2.0 * 6371 * math.pi / 360.0)
    vzdalenost_km = round(vzdalenost_km, 2)
    return vzdalenost_km

poloha_nadrazi_opava = [49.9345092, 17.9085369]

sportoviste["vzdalenost_od_nadrazi_v_km"] = sportoviste.apply(vzdalenost_od_bodu, axis=1, args=(poloha_nadrazi_opava,))

print(sportoviste.head())
