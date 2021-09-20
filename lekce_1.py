import pandas
import requests
import matplotlib.pyplot as plt
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/sales_plan.csv")
open("sales_plan.csv", 'wb').write(r.content)

df_plan = pandas.read_csv("sales_plan.csv")
df_plan["sales_plan_cumsum"] = df_plan.groupby("year")["sales"].cumsum()
# print(df_plan)
# print(df_plan.head())
# print(df_plan.tail())

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/sales_actual.csv")
open("sales_actual.csv", 'wb').write(r.content)

df_actual = pandas.read_csv("sales_actual.csv")
df_actual["date"] = pandas.to_datetime(df_actual["date"])
df_actual["month"] = df_actual["date"].dt.month
df_actual["year"] = df_actual["date"].dt.year
print(df_actual.columns)
print(df_actual.head())

df_actual_grouped = df_actual.groupby(["month", "year"]).sum()
df_actual_grouped["sales_actual_cumsum"] = df_actual_grouped["contract_value"].cumsum()
df_actual_grouped = df_actual_grouped.reset_index()
# print(df_actual_grouped.head())

df_joined = pandas.merge(df_plan, df_actual_grouped, on=["month", "year"])
df_joined = df_joined.set_index("month")
# print(df_joined)

# ax = df_joined.plot(color="red", y="sales_plan_cumsum", title="Skutečné vs plánované tržby")
# df_joined.plot(kind="bar", y="sales_actual_cumsum", ax=ax)
df_joined.plot(kind="bar", y=["sales_plan_cumsum", "sales_actual_cumsum"])
# plt.show()

df_actual_pivot = pandas.pivot_table(df_actual, index="country", columns="sales_manager", values="contract_value", aggfunc=numpy.sum)
print(df_actual_pivot)
