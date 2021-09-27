import pandas as pd
import requests
import numpy as np

desired_width = 1000
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',100)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/baroko_half_marathon.csv")
open("baroko_half_marathon.csv", 'wb').write(r.content)
baroko_half_marathon = pd.read_csv("baroko_half_marathon.csv")

# V souboru baroko_half_marathon.csv najdeš výsledky Baroko půlmaratonu, který se běží každý rok na začátku září. Tvým
# úkolem je vzít výsledky za dva po sobě jdoucí roky a porovnat výkony běžců, kteří se zúčastnili obou závodů. Závěrem
# analýzy bude zjištění, kolik běžců se meziročně zlepšilo a kolik zhoršilo.

# - Data musíš nejprve seřadit. Seřaď data dle jména závodníka, ročíku a roku závodu.
baroko_half_marathon = baroko_half_marathon.sort_values(["Jméno závodníka", "Ročník", "Rok závodu"])

# - Nyní pracuj se sloupcem FINISH, který obsahuje čas závodníka. Převeď tento sloupec na typ datetime.
# Nemusíš používat žádný formátovací řetězec.
baroko_half_marathon["FINISH"] = pd.to_datetime(baroko_half_marathon["FINISH"])

# - Použij metodu shift, abys získal(a) na stejném řádku časy závodníka v obou letech. Aby se ti ale nepomíchaly časy
# rozdílných závodníků, aplikuj metodu groupby(), jako jsme to udělali u dat indexu ekonomické svobody.
baroko_half_marathon["FINISH předchozí rok"] = baroko_half_marathon.groupby(["Jméno závodníka", "Ročník"])["FINISH"].shift()

# - Z tabulky odstraň data závodníků, kteří se zúčastnili pouze jednoho za závodů, a řádky s daty z roku 2019.
# Můžeš použít třeba metodu dropna() a jedním příkazem se zbavit všech zbytečných řádků.
baroko_half_marathon = baroko_half_marathon.dropna(axis=0, subset=['FINISH předchozí rok']).reset_index(drop=True)

# - Vypočti rozdíl mezi časy závodníků v letech 2019 a 2020.
baroko_half_marathon["Rozdíl časů"] = baroko_half_marathon["FINISH"] - baroko_half_marathon["FINISH předchozí rok"]

# - Vypočítej, kolik závodníků si svůj čas zlepšilo a kolik zhoršilo. Při dotazu na porovnávání můžeš sloupec s časovým
# rozdílem porovnat s hodnotou pandas.Timedelta("P0D"), což je nulová změna. Pomocí tohoto porovnání jasně odlišíš,
# kteří závodníci se zlepšili a kteří zhoršili.
baroko_half_marathon["Zlepšení / Zhoršení"] = np.where(baroko_half_marathon["Rozdíl časů"] < pd.Timedelta("P0D"), "zhoršil se", "zlepšil se")
zlepseni_zhorseni = baroko_half_marathon['Zlepšení / Zhoršení'].value_counts()
print(zlepseni_zhorseni)