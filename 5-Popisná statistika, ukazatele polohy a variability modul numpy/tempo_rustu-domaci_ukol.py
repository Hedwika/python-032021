import requests
import pandas as pd
from scipy.stats import stats

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
open("crypto_prices.csv", "wb").write(r.content)
crypto_prices = pd.read_csv("crypto_prices.csv")

crypto_prices["Change"] = crypto_prices.groupby("Symbol")["Close"].pct_change()

# Z datového souboru si vyber jednu kryptoměnu a urči průměrné denní tempo růstu měny za sledované období. Můžeš využít
# funkci geometric_mean z modulu statistics. Vyber si sloupec se změnou ceny, kterou máš vypočítanou z předchozího
# cvičení (případně si jej dopočti), přičti k němu 1 (nemusíš dělit stem jako v lekci, hodnoty jsou jako desetinná
# čísla, nikoli jako procenta) a převeď jej na seznam pomocí metody .tolist().
crypto_prices_aave = crypto_prices[crypto_prices["Symbol"] == "AAVE"]
crypto_prices_aave["Change"] = (crypto_prices_aave["Change"] + 1)
crypto_prices_aave = crypto_prices_aave.dropna()
crypto_prices_aave_list = crypto_prices_aave["Change"].tolist()

# Následně vypočti geometrický průměr z těchto hodnot.
print(stats.gmean(crypto_prices_aave_list) - 1)

# Zkus spočítat průměrné tempo růstu pro všechny měny. Využij k tomu metodu apply v kombinaci s funkcí stats.gmean,
# která je součástí modulu scipy (ten je instalován automaticky spolu s pandas, takže ho nemusíš instalovat).
crypto_prices = crypto_prices.dropna()
crypto_prices["Date"] = pd.to_datetime(crypto_prices["Date"])
crypto_prices["growth"] = crypto_prices.Change.astype(float) + 1
growth_all = crypto_prices.groupby("Symbol").agg({"growth": [stats.gmean]})
print(growth_all - 1)