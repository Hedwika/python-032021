import yfinance as yf
import pandas
import seaborn
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

msft = yf.Ticker("MSFT")
msft_df = msft.history(period="1y")
# print(msft_df.describe())

aapl = yf.Ticker("AAPL")
aapl_df = aapl.history("1y")

msft_close = msft_df["Close"]
aapl_close = aapl_df["Close"]
stock_data_df = pandas.merge(msft_close, aapl_close, on=["Date"], suffixes=["MSFT", "AAPL"])
stock_data_df = stock_data_df.rename(columns={"CloseMSFT": "MSFT", "CloseAAPL": "AAPL"})
stock_data_change_df = stock_data_df.pct_change()
# print(stock_data_change_df.describe())

seaborn.jointplot("MSFT", "AAPL", stock_data_change_df, kind='scatter', color='seagreen')
plt.show()

tsn = yf.Ticker("TSN")
tsn_df = tsn.history(period="1y")
tsn_df = tsn_df.rename(columns={"Close": "TSN"})
tsn_close = tsn_df["TSN"]
stock_data_three_df = pandas.merge(stock_data_df, tsn_close, on=["Date"])
stock_data_three_df.head()
seaborn.jointplot("AAPL", "TSN", stock_data_three_df.pct_change(), kind='scatter', color='seagreen')
plt.show()

print(stock_data_three_df.corr())

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(3, 1)

ax = fig.add_subplot(gs[0, 0])
ax.hist(stock_data_three_df["AAPL"])

ax = fig.add_subplot(gs[1, 0])
ax.hist(stock_data_three_df["MSFT"])

ax = fig.add_subplot(gs[2, 0])
ax.hist(stock_data_three_df["TSN"])

plt.show()

print(stock_data_three_df.skew())