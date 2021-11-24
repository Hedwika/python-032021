import requests
from scipy.stats import mannwhitneyu
import pandas as pd

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/psenice.csv") as r:
  open("psenice.csv", 'w', encoding="utf-8").write(r.text)

# V souboru jsou data o délce zrn pšenice v milimetrech pro dvě odrůdy - Rosa a Canadian. Proveď statistický test
# hypotézy o tom, zda se délka těchto dvou zrn liší. K testu použij Mann–Whitney U test, který jsme používali na lekci.

# 1) V komentáři u programu formuluj hypotézy, které budeš ověřovat. Je potřeba formulovat dvě hypotézy - nulovou
# a alternativní. Provádíme oboustranný test, takže alternativní hypotézy by měla být, že průměry délky zrna jsou
# různé (nejsou si rovné).

# Hladina významnosti: 5 %
# Nulová hypotéza: Délky zrna jsou stejné.
# Alternativní hypotéza: Průměry délky zrna Rosa jsou větší než u odrůdy Canadian.

# 2) Pomocí modulu scipy urči p-hodnotu testu a porovnej ji s hladinou významnosti 5 %. V komentáři uveď závěr,
# jestli nulovou hypotézu na základě p-hodnoty zamítáme.
psenice_df = pd.read_csv("psenice.csv")

x = psenice_df["Rosa"]
y = psenice_df["Canadian"]
print(mannwhitneyu(x, y))

# Hladina významnosti je vyšší než p-hodnota, proto nulovou hypotézu zamítáme.