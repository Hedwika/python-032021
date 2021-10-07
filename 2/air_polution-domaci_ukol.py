import requests
import pandas as pd

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
#   open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

air_polution = pd.read_csv("air_polution_ukol.csv")

# Jemné částice
# V souboru air_polution_ukol.csv najdeš data o množství jemných částic změřených v ovzduší v jedné
# plzeňské meteorologické stanici.
# 1) Načti dataset a převeď sloupec date (datum měření) na typ datetime.
invoices["invoice_date_converted"] = pandas.to_datetime(invoices["invoice_date"])
invoices.head()
print(air_polution.head())

# 2) Přidej sloupce s rokem a číslem měsíce, které získáš z data měření.


# 3) Vytvoř pivot tabulku s průměrným počtem množství jemných částic (sloupec pm25) v jednotlivých měsících a jednotlivých letech. Jako funkci pro agregaci můžeš použít numpy.mean.


# Dobrovolný doplněk
# Podívej se do první lekce na část o teplotních mapách a zobrat výsledek analýzy jako teplotní mapu.
# Použij metodu dt.dayofweek a přidej si do sloupce den v týdnu. Číslování je od 0, tj. pondělí má číslo 0 a neděle 6. Porovnej, jestli se průměrné množství jemných částic liší ve všední dny a o víkendu.