import requests
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.ar_model import AutoReg

# Stáhni si data o průměrném denním odebíraném výkonu elektrické energie v MW, která poskytla společnost
# PJM Interconnection LLC.
r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/PJME_daily.csv")
with open("PJME_daily.csv", "wb") as f:
  f.write(r.content)
pjme_daily_df = pd.read_csv("PJME_daily.csv")
# print(pjme_daily_df)

pjme_daily_df = pjme_daily_df.set_index("Date")
# pjme_daily_df.plot()
# plt.show()

# - Vyber data za posledních 100 dní a pokus se řadu vyrovnat pomocí klouzavých průměrů. Vhodně nastav sezónnost dat.
# Výsledek si zobraz pomocí grafu.
pjme_daily_df = pjme_daily_df.tail(100)
print(pjme_daily_df)
# pjme_daily_df.plot()
# plt.show()

pjme_daily_df["SMA_7"] = pjme_daily_df["PJME_MW"].rolling(7).mean()
# pjme_daily_df[["SMA_7", "PJME_MW"]].plot()
# plt.show()

# - Použij exponenciální vyrovnávání k vyhlazení časové řady a výsledek si opět zobraz jako graf. Vyzkoušej několik
# hodnot parametru alpha.
pjme_daily_df["EMA"] = pjme_daily_df["PJME_MW"].ewm(alpha=0.01).mean()
# pjme_daily_df[["EMA", "PJME_MW"]].plot()
# plt.show()

# - Pomocí grafu si zobraz, jaká je autokorelace časové řady.
# plot_acf(pjme_daily_df["PJME_MW"])
# plt.show()

# - Agreguj data po měsících dat, aby hodnota za každý měsíc představovala průměrný odebíraný výkon za všechny dny
# měsíce. Opět aplikuj klouzavý průměr a výsledek si zobraz jako graf.
pjme_daily_df = pjme_daily_df.reset_index()
pjme_daily_df["Month"] = pd.to_datetime(pjme_daily_df["Date"]).dt.strftime("%Y/%m")
pjme_daily_df_grouped = pjme_daily_df.groupby("Month")["PJME_MW"].mean()
pjme_daily_df_grouped = pd.DataFrame(pjme_daily_df_grouped)
# print(pjme_daily_df_grouped)

pjme_daily_df_grouped["SMA_12"] = pjme_daily_df_grouped["PJME_MW"].rolling(7).mean()
pjme_daily_df_grouped["CMA_12"] = pjme_daily_df_grouped["PJME_MW"].rolling(7, center=True).mean()
# pjme_daily_df_grouped[["PJME_MW", "SMA_12", "CMA_12"]].plot()
# plt.show()

# - Na data agregovaná dle měsíce aplikuj dekompozici časové řady (aditivní model) a výsledek zobraz jako graf.
# decompose = seasonal_decompose(pjme_daily_df_grouped['PJME_MW'], model='additive', period=7)
# decompose.plot()
# plt.show()
# Nefunguje, protože data nemají trend

# - Vrať se k časové řadě s denními údaji. Pomocí autoregresního modelu zkus predikovat spotřebu na dva týdny dopředu.
model = AutoReg(pjme_daily_df['PJME_MW'], lags=10, trend="t", seasonal=True, period=7)
model_fit = model.fit()
predictions = model_fit.predict(start=pjme_daily_df.shape[0], end=pjme_daily_df.shape[0] + 7)
df_forecast = pd.DataFrame(predictions, columns=["Prediction"])
df_with_prediction = pd.concat([pjme_daily_df, df_forecast])
df_with_prediction[["PJME_MW", "Prediction"]].plot()
plt.show()