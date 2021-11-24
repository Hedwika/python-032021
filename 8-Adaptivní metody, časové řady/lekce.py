import pandas
import matplotlib.pyplot as plt
import requests
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.ar_model import AutoReg

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/AirPassengers.csv")
with open("AirPassengers.csv", "wb") as f:
  f.write(r.content)

air_passengers_df = pandas.read_csv("AirPassengers.csv")

# Klouzavé průměry
air_passengers_df = air_passengers_df.rename({"#Passengers": "Passengers"}, axis=1)
air_passengers_df = air_passengers_df.set_index("Month")
air_passengers_df["SMA_12"] = air_passengers_df["Passengers"].rolling(12).mean()

# CMA = centrované klouzavé průměry, kde je hodnota průměru umístěna uprostřed periody.
air_passengers_df["CMA_12"] = air_passengers_df["Passengers"].rolling(12, center=True).mean()

air_passengers_df["EMA"] = air_passengers_df["Passengers"].ewm(alpha=0.03).mean()
# air_passengers_df[["EMA", "SMA_12", "CMA_12", "Passengers"]].plot()

mod = ExponentialSmoothing(air_passengers_df["Passengers"], seasonal_periods=12, trend="add", seasonal="add",
                           use_boxcox=True, initialization_method="estimated",)
res = mod.fit()
air_passengers_df["HM"] = res.fittedvalues
# air_passengers_df[["HM", "Passengers"]].plot()

df_forecast = pandas.DataFrame(res.forecast(24), columns=["Prediction"])
df_with_prediction = pandas.concat([air_passengers_df, df_forecast])
# df_with_prediction[["Passengers", "Prediction"]].plot()
# plt.show()

# Autokorelace
# lag nastavujeme, jak vzdálené hodnoty mají být pro výpočet autokorelace použity. Např. 1 znamena, že je zjišťována
# síla lineární závislosti mezi dvěma po sobně následujícími hodnotami. Většinou platí, že čím vzdálenější hodnoty
# porovnáváme, tím je míra lineární závislosti slabší.
print(air_passengers_df["Passengers"].autocorr(lag=1))
# plot_acf(air_passengers_df["Passengers"])
# plt.show()

# Dekompozice časové řady
# model = additive:
decompose = seasonal_decompose(air_passengers_df['Passengers'], model='additive', period=12)
# model = multiplicative: uvažuje procenta (např. 1.2 znamená 20 % nad trendem)
decompose = seasonal_decompose(air_passengers_df['Passengers'], model='multiplicative', period=12)
# decompose.plot()
# plt.show()

# Autoregresivní modely
# Vycházejí z předpokladu, že hodnoty časové řady jsou závislé na jejích vlastních hodnotách v minulosti.
model = AutoReg(air_passengers_df['Passengers'], lags=10, trend="ct", seasonal=True, period=12)
res = model.fit()
predictions = res.predict(start=air_passengers_df.shape[0], end=air_passengers_df.shape[0] + 12)
df_forecast = pandas.DataFrame(predictions, columns=["Prediction"])
df_with_prediction = pandas.concat([air_passengers_df, df_forecast])
df_with_prediction[["Passengers", "Prediction"]].plot()
plt.show()