import requests
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# Stáhni si soubor MLTollsStackOverflow.csv, který obsahuje počty položených otázek na jednotlivé programovací techniky
# a další technologie.
r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/MLTollsStackOverflow.csv")
with open("MLTollsStackOverflow.csv", "wb") as f:
  f.write(r.content)
mltollsstackoverflow_df = pd.read_csv("MLTollsStackOverflow.csv")
print(mltollsstackoverflow_df)

# - Vyber sloupec python.
python_df = mltollsstackoverflow_df[["python"]]
print(python_df)

# - Proveď dekompozici této časové řady pomocí multiplikativního modelu. Dekompozici zobraz jako graf.
decompose = seasonal_decompose(python_df["python"], model='multiplicative', period=12)
decompose.plot()
plt.show()

# - Vytvoř predikci hodnot časové řady pomocí Holt-Wintersovy metody na 12 měsíců. Sezónnost nastav jako 12 a uvažuj
# multiplikativní model pro trend i sezónnost. Výsledek zobraz jako graf.
mod = ExponentialSmoothing(python_df["python"], seasonal_periods=12, trend="add", seasonal="add", use_boxcox=True, initialization_method="estimated",)
res = mod.fit()
# python_df["HM"] = res.fittedvalues
# print(python_df)
# python_df[["HM", "python"]].plot()
# plt.show()

df_forecast = pd.DataFrame(res.forecast(12), columns=["Prediction"])
df_with_prediction = pd.concat([python_df, df_forecast])
df_with_prediction[["python", "Prediction"]].plot()
plt.show()
