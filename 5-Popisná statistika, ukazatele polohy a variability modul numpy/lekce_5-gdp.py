import statistics
import matplotlib.pyplot as plt

gdp_growth_rate = [
  2.435,
  1.76,
  -0.785,
  -0.046,
  2.262,
  5.388,
  2.537,
  5.169,
  3.199,
  2.314
]

# Abychom mohli zjisti průměrné tempo růstu v tomto období, musíme nejprve převést na index růstu. Převod provedeme tak,
# že ke každé hodnotě procentuálního růstu připočteme 1 a růst v procentech vydělíme 100. Výslednou hodnotu pak opačným
# způsobem převedeme na procenta.
gdp_growth = []
for value in gdp_growth_rate:
  gdp_growth.append(1 + value/100)

# Geometrický průměr má tu vlastnost, že pokud bychom vzali hrubý domácí produkt v roce 2010 a vynásobili ho číslem 9
# a průměrným tempem růstu, získáme velikost hrubého domácího produktu v roce 2019. Podobně bychom například získali
# částku na bankovním účtě na základě průměrné úrokové míry. Aritmetický průměr takovou vlastnost nemá.
print((statistics.geometric_mean(gdp_growth) - 1) * 100)