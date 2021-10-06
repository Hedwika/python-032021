import requests
import pandas as pd

desired_width = 1000
pandas.set_option('display.width', desired_width)
pandas.set_option('display.max_columns',100)

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/1976-2020-president.csv") as r:
  open("1976-2020-president.csv", 'w', encoding="utf-8").write(r.text)

swing_states = pd.read_csv("1976-2020-president.csv")
print(swing_states.head())