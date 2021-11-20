import requests
import pandas as pd
import seaborn as sns
import matplotlib as plt

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

air_polution = pd.read_csv("air_polution_ukol.csv")

# Jemné částice
# V souboru air_polution_ukol.csv najdeš data o množství jemných částic změřených v ovzduší v jedné
# plzeňské meteorologické stanici.
# 1) Načti dataset a převeď sloupec date (datum měření) na typ datetime.
air_polution["date_converted"] = pd.to_datetime(air_polution["date"])

# 2) Přidej sloupce s rokem a číslem měsíce, které získáš z data měření.
air_polution["year"] = air_polution["date_converted"].dt.year
air_polution["month"] = air_polution["date_converted"].dt.month

# 3) Vytvoř pivot tabulku s průměrným počtem množství jemných částic (sloupec pm25) v jednotlivých měsících a jednotlivých letech.
# Jako funkci pro agregaci můžeš použít numpy.mean.
air_polution_aggregated_mean = air_polution.groupby(["year", "month"])["pm25"].mean()
print(air_polution_aggregated_mean.head())

# Dobrovolný doplněk
# 1) Podívej se do první lekce na část o teplotních mapách a zobraz výsledek analýzy jako teplotní mapu.
ax = sns.heatmap(air_polution_aggregated_mean, annot=True, fmt=".1f", linewidths=.5, cmap="YlGn")
plt.show()

# 2) Použij metodu dt.dayofweek a přidej si do sloupce den v týdnu. Číslování je od 0, tj. pondělí má číslo 0 a neděle 6.
# Porovnej, jestli se průměrné množství jemných částic liší ve všední dny a o víkendu.