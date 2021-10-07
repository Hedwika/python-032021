import requests
import pandas as pd

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv")
# open("lexikon-zvirat.csv", "wb").write(r.content)

lexikon_zvirat = pd.read_csv("lexikon-zvirat.csv", sep=";")
print(lexikon_zvirat.head())