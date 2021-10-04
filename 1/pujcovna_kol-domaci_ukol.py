import requests
import pandas as pd
import numpy as np

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/london_merged.csv")
open("london_merged.csv", 'wb').write(r.content)

london_bike_rental = pd.read_csv("london_merged.csv")

# Půjčování kol
# V souboru london_merged.csv najdeš informace o počtu vypůjčení jízdních kol v Londýně.
# Vytvoř sloupec, do kterého z časové značky (sloupec timestamp) ulož rok.
london_bike_rental["date"] = pd.to_datetime(london_bike_rental["timestamp"])
london_bike_rental["year"] = london_bike_rental["date"].dt.year

# Vytvoř kontingenční tabulku, která porovná kód počasí (sloupec weather_code se sloupcem udávající rok.
# Definice jednotlivých kódů jsou:
# 1 = Clear ; mostly clear but have some values with haze/fog/patches of fog/ fog in vicinity
# 2 = scattered clouds / few clouds
# 3 = Broken clouds
# 4 = Cloudy
# 7 = Rain/ light Rain shower/ Light rain
# 10 = rain with thunderstorm
# 26 = snowfall
# 94 = Freezing Fog
london_bike_rental_pivot = pd.pivot_table(london_bike_rental, values="cnt", index="weather_code", columns="year", aggfunc=np.sum, margins=True)
print("Četnost půjčení kol byla za sledovaného počasí v jednotlivých letech následující:")
print(london_bike_rental_pivot)

# Rozšířené zadání
# Rozšířená zadání jsou čistě pro dobrovolníky, kteří mají hodně času a hledají větší výzvu :-)
# Jako hodnoty v kontingenční tabulce zobraz relativní počty jízd pro jednotlivé kódy počasí v jednom roce.
# Příklad možného výsledku by byl: v roce 2020 proběhlo 40 % jízd za počasí s kódem 1, 20 % jízd za počasí s kódem 2
# a 40 % jízd za počasí s kódem 3 atd.
london_bike_rental_pivot_percentage = london_bike_rental_pivot.div( london_bike_rental_pivot.iloc[-1,:], axis=1)
print("Poměr půjčení kol za sledovaného počasí byl v jednotlivých letech následující:")
print(london_bike_rental_pivot_percentage)