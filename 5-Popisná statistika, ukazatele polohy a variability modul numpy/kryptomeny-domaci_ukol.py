import statistics
import requests
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from scipy.stats import gmean
from scipy import stats

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)
crypto_prices = pd.read_csv("crypto_prices.csv")

# V souboru crypto_prices.csv najdeš ceny různých kryptoměn v průběhu času. Datum je ve sloupci Date a název kryptoměny
# ti prozradí sloupec Name, alternativně můžeš využít sloupec Symbol.
#
# 1) Použij zavírací cenu kryptoměny (sloupec Close) a vypočti procentuální změnu jednotlivých kryptoměn. Pozor na to,
# ať se ti nepočítají ceny mezi jednotlivými měnami. Ošetřit to můžeš pomocí metody groupby(), jako jsme to dělali
# např. u metody shift().
crypto_prices["Change"] = crypto_prices.groupby("Symbol")["Close"].pct_change()

# # 2) Vytvoř korelační matici změn cen jednotlivých kryptoměn a zobraz je jako tabulku.
crypto_prices_pivot = crypto_prices.pivot(index = "Date", columns = "Symbol", values="Change")
crypto_prices_corr = crypto_prices_pivot.corr()

# 3) V tabulce vyber dvojici kryptoměn s vysokou hodnotou koeficientu korelace a jinou dvojici s koeficientem korelace
# blízko 0. Změny cen pro dvojice měn, které jsou hodně a naopak málo korelované, si zobraz jako bodový graf.
wbtc_eth = crypto_prices_corr[["WBTC", "ETH"]]
seaborn.jointplot("WBTC", "ETH", wbtc_eth, kind="scatter")
plt.show()

uni_doge = crypto_prices_corr[["UNI", "DOGE"]]
seaborn.jointplot("UNI", "DOGE", uni_doge, kind="scatter")
plt.show()

# Dobrovolný doplněk
# 1) Vyzkoušej aplikovat Spearmenovu korelaci a porovnej, nakolik se liší výsledky.
crypto_prices_corr_spearman = crypto_prices.corr(method="spearman")
print(crypto_prices_corr_spearman)

# 2) Vyzkoušej si spočítat korelaci pro nějaké kratší časové období (například 1 měsíc) a pro dvě nejvíce a nejméně
# korelované hodnoty si zobraz vývoj zavírací ceny v čase (jako liniový graf). Je možné korelaci vyčíst z tohoto grafu?
crypto_prices_month = crypto_prices.tail(30)
crypto_prices_corr_month = crypto_prices_month.corr()
print(crypto_prices_corr_month)

ltc = crypto_prices_month["LTC"]
eos = crypto_prices_month["EOS"]
plt.plot(ltc, label="LTC", color="silver")
plt.plot(eos, label="EOS", color="black")
plt.show()

aave = crypto_prices_month["AAVE"]
doge = crypto_prices_month["DOGE"]
plt.plot(aave, label="AAVE", color="blue")
plt.plot(doge, label="DOGE", color="yellow")
plt.show()