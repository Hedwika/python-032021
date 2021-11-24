import requests
import pandas as pd
from scipy.stats import mannwhitneyu

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

# V souboru air_polution_ukol.csv najdeš data o množství jemných částic změřených v ovzduší v jedné plzeňské
# meteorologické stanici a který jsme již používali v úkolu z druhého týdne.
#
# Pokud máš úkol hotový, můžeš si z něj zkopírovat následující krok:
#
# Načti dataset a převeď sloupec date (datum měření) na typ datetime.
air_polution_df = pd.read_csv("air_polution_ukol.csv")
air_polution_df["date_converted"] = pd.to_datetime(air_polution_df["date"])

# Dále pokračuj následujícími kroky:
#
# Z dat vyber data za leden roku 2019 a 2020.
x = air_polution_df[air_polution_df["date_converted"].between("2019-01-01", "2019-01-31")]["pm25"]
y = air_polution_df[air_polution_df["date_converted"].between("2020-01-01", "2020-01-31")]["pm25"]

# Porovnej průměrné množství jemných částic ve vzduchu v těchto dvou měsících pomocí Mann–Whitney U testu.
print(mannwhitneyu(x, y))

# Formuluj hypotézy pro oboustranný test (nulovou i alternativní) a napiš je do komentářů v programu.

# Hladina významnosti: 5 %
# Nulová hypotéza: Hodnota ukazatele pm25 byla v lednu 2019 stejná jako v lednu 2020.
# Alternativní hypotéza: Hodnota ukazatele pm25 byla v lednu 2019 vyšší než v lednu 2020.

# Rozhodni, zda bys na hladině významnosti 5 % zamítla nulovou hypotézu. Své rozhodnutí napiš do programu.
# Hladina významnosti je vyšší než p-hodnota, proto nulovou hypotézu zamítáme.