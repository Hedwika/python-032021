import numpy
from scipy.stats import binom
import pandas
import requests
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

# pravděpodobnost 2 úspěchů na 3 pokusnech, pravděpodobnost úspěchu je 0.5
print(binom.pmf(2, 3, 0.5))

p = 0.5
n = list(range(1, 11))
y = binom.pmf(n, n, 0.5)
data = pandas.DataFrame(y)
data["Color"] = numpy.where(data[0] > 0.05, "blue", "red")
data[0].plot(kind="bar", color=data["Color"])
# plt.show()

# p-hodnota: říká, jaká je pravděpodobnost pozorovaného či ještě více extrémního výsledku za předpokladu platnosti nulové hypotézy?
# Dole: pravděpodobnost 9 úspěšných pokusů + pravděpodobnost 10 úspěšných pokusů. Výsledek = p-hodnota
print(binom.pmf(k=9, n=10, p=0.5) + binom.pmf(k=10, n=10, p=0.5))
#  Je-li p-hodnota nižší než hladina významnosti, zamítáme nulovou hypotézu. V opačném případě ji nezamítáme.
# V našem konkrétním pokusu bychom hladině významnosti 5 % bychom nulovou hypotézu zamítli,
# na hladině významnosti 1 % však nikoli.

# Oboustranný test
print(binom.pmf(k=0, n=5, p=0.5) + binom.pmf(k=5, n=5, p=0.5))

# příklady statistických testů
r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/student-mat.csv")
open("student-mat.csv", "wb").write(r.content)

data = pandas.read_csv("student-mat.csv")
print(data.head())

x = data[data["school"] == "GP"]["G1"]
y = data[data["school"] == "MS"]["G1"]
print(x.shape)
print(y.shape)
print(mannwhitneyu(x, y))
# Funkce vrací p-hodnotu (pvalue=0.2821166028357025) a hodnotu statistiky. Pokud bychom uvažovali hladinu
# významnosti 5 %, nulovou hypotézu bychom nezamítli.
#
# Zkusme nyní rozdělit studenty na skupiny podle toho, jestli mají zájem pokračovat ve studiu (sloupec higher).
# Hypotézy budou následující:
# H0: Průměrný počet bodů je stejný pro obě skupiny.
# H1: Průměrný počet bodů je vyšší u studentů, kteří mají zájem se dále vzdělávat.

data = pandas.read_csv("student-mat.csv")
x = data[data["higher"] == "yes"]["G1"]
y = data[data["higher"] == "no"]["G1"]
print(mannwhitneyu(x, y, alternative="greater"))
# p-hodnota testu je velmi nízká a pro hladinu významnosti 5 % bychom nulovou hypotézu zamítli. Tvrdíme tedy,
# že studenti, kteří mají zájem pokračovat ve studiu, získali v průměru vyšší počet bodů.