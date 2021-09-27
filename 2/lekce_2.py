import datetime
import pandas
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# vidět celé číslo
pd.set_option('float_format', '{:f}'.format)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/data_with_ids.csv")
open("data_with_ids.csv", 'wb').write(r.content)

# odstranění duplicit
data_with_ids = pd.read_csv("data_with_ids.csv")
data_with_ids_unique = data_with_ids.drop_duplicates(ignore_index=True)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/covid_data.csv")
open("covid_data.csv", 'wb').write(r.content)
covid_data = pd.read_csv("data_with_ids.csv")
covid_data_unique = covid_data.drop_duplicates(subset=["date"], keep="last")

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/invoices.csv")
open("invoices.csv", 'wb').write(r.content)

# Přidání dní k datu
invoices = pd.read_csv("invoices.csv")
invoices["invoice_date_converted"] = pandas.to_datetime(invoices["invoice_date"], format="%d. %m. %Y")
# invoices["due_date"] = invoices["invoice_date_converted"] + pandas.Timedelta("60 days")
invoices["due_date"] = invoices["invoice_date_converted"] + pandas.Timedelta("P60D")
# today_date = datetime.datetime(2021, 9, 1)
today_date = datetime.datetime.now()
invoices["status"] = np.where(invoices["due_date"] < today_date, "po splatnosti", "před splatností")
# print("Objem faktur po splatnosti a před splatností")
# print(invoices.groupby("status")["amount"].sum())

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/invoices_2.csv")
open("invoices_2.csv", 'wb').write(r.content)
invoices_2 = pd.read_csv("invoices_2.csv")

# Průměrná doba splacení faktury
invoices_2["invoice_date"] = pandas.to_datetime(invoices_2["invoice_date"], format="%d. %m. %Y")
invoices_2["payment_date"] = pandas.to_datetime(invoices_2["payment_date"], format="%d. %m. %Y")
invoices_2_paid = invoices_2.dropna().reset_index(drop=True)
invoices_2_paid["paid_in"] = invoices_2["payment_date"] - invoices_2["invoice_date"]
average_payment_data = invoices_2_paid.groupby(["customer"])["paid_in"].mean()
average_payment_data = pandas.DataFrame(average_payment_data)


invoices_2_not_paid = invoices_2[invoices_2["payment_date"].isna()]
invoices_2_not_paid = pandas.merge(invoices_2_not_paid, average_payment_data, on=["customer"], how="outer")
invoices_2_not_paid["expended_payment_date"] = invoices_2_not_paid["invoice_date"] + invoices_2_not_paid["paid_in"]
invoices_2_not_paid["expended_payment_date"] = invoices_2_not_paid["expended_payment_date"].dt.date


r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/signal_monitoring.csv")
open("signal_monitoring.csv", 'wb').write(r.content)
signal_monitoring = pd.read_csv("signal_monitoring.csv")

signal_monitoring["event_date_time"] = pandas.to_datetime(signal_monitoring["event_date_time"])
signal_monitoring["event_date_time_2"] = signal_monitoring["event_date_time"].shift(-1)
signal_monitoring["event_length"] = signal_monitoring["event_date_time_2"] - signal_monitoring["event_date_time"]
signal_monitoring = signal_monitoring[signal_monitoring["event_type"] == "signal lost"]

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/ioef.csv")
open("ioef.csv", 'wb').write(r.content)
ioef = pd.read_csv("ioef.csv")

# Hodnocení v rámci Evropy v různých letech
ioef["Rank"] = ioef.groupby(["Index Year"])["Overall Score"].rank(ascending=False)

# Seřazení stejných států z jiných let k sobě a rozdíl v letech
ioef = ioef.sort_values(["Name", "Index Year"])
ioef["Rank Previous Year"] = ioef.groupby(["Name"])["Rank"].shift()
ioef["Difference"] = ioef["Rank"] - ioef["Rank Previous Year"]
print(ioef)