import requests
import pandas as pd

desired_width = 1000
pandas.set_option('display.width', desired_width)
pandas.set_option('display.max_columns',100)

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
  open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

air_polution = pd.read_csv("air_polution_ukol.csv")
print(air_polution.head())