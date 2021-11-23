import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AutoReg
import numpy as np
from pandas.plotting import lag_plot
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# Pomocí modulu yfinance, který jsme používali v 5. lekci, stáhni ceny akcií společnosti Cisco
# (používají "Ticker" CSCO) za posledních 5 let. Dále pracuj s cenami akcie v závěru obchodního dne,
# tj. použij sloupec "Close".
csco = yf.Ticker("CSCO")
csco_df = csco.history(period="5y")
csco_df = csco_df[["Close"]]

# - Zobraz si graf autokorelace a podívej se, jak je hodnota ceny závislná na svých vlastních hodnotách v minulosti.
# plot_acf(csco_df["Close"])
# plt.show()

# - Zkus použít AR model k predikci cen akcie na příštích 5 dní.
# model = AutoReg(csco_df['Close'], lags=10, trend="t", seasonal=True, period=7)
# model_fit = model.fit()
# predictions = model_fit.predict(start=csco_df.shape[0], end=csco_df.shape[0] + 5)
# df_forecast = pd.DataFrame(predictions, columns=["Prediction"])
# df_with_prediction = pd.concat([csco_df, df_forecast])
# df_with_prediction[["Close", "Prediction"]].plot()
# plt.show()

# - Zobraz v grafu historické hodnoty (nikoli celou řadu, ale pro přehlednost např. hodnoty za posledních 50 dní)
# a tebou vypočítanou predikci.
# df_with_prediction = df_with_prediction.tail(55)
# df_with_prediction[["Close", "Prediction"]].plot()
# plt.show()

# Rozšířené zadání
# Pokud bys měl(a) zájem prostuduj si článek [Time-Series Forecasting: Predicting Stock Prices Using An ARIMA Model]
# (https://towardsdatascience.com/time-series-forecasting-predicting-stock-prices-using-an-arima-model-2e3b3080bd70),
# kde je k predikci ceny akcie použit ARIMA model, a zkus použít tento model k predikci akcie firmy Cisco.
train_data, test_data = csco_df[0:int(len(csco_df)*0.7)], csco_df[int(len(csco_df)*0.7):]
training_data = train_data['Close'].values
test_data = test_data['Close'].values
history = [x for x in training_data]
model_predictions = []
N_test_observations = len(test_data)
for time_point in range(N_test_observations):
    model = ARIMA(history, order=(4,1,0))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    model_predictions.append(yhat)
    true_test_value = test_data[time_point]
    history.append(true_test_value)
MSE_error = mean_squared_error(test_data, model_predictions)
print('Testing Mean Squared Error is {}'.format(MSE_error))

test_set_range = csco_df[int(len(csco_df)*0.7):].index
plt.plot(test_set_range, model_predictions, color='blue', marker='o', linestyle='dashed',label='Predicted Price')
plt.plot(test_set_range, test_data, color='red', label='Actual Price')
plt.title('CISCO Prices Prediction')
plt.xlabel('Date')
plt.ylabel('Prices')
# plt.xticks(np.arange(881,1259,50), csco_df.Date[881:1259:50])
plt.legend()
plt.show()