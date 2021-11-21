import requests
import pandas as pd
import statsmodels.formula.api as smf

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# V souboru Fish.csv najdeš informace o rybách z rybího trhu:
#
# délku (vertikální - Length1, diagonální - Length2 a úhlopříčnou - Length3),
# výšku,
# šířku,
# živočišný druh ryby,
# hmnotnost ryby.
r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Fish.csv")
with open("Fish.csv", "wb") as f:
  f.write(r.content)
ryby_df = pd.read_csv("Fish.csv")
# print(ryby_df)

# Vytvoř regresní model, který bude predikovat hmnotnost ryby na základě její diagonální délky (sloupec Length2).
mod = smf.ols(formula="Weight ~ Length2", data=ryby_df)
res = mod.fit()
# print(res.summary())

# Zkus přidat do modelu výšku ryby (sloupec Height) a porovnej, jak se zvýšila kvalita modelu.
mod = smf.ols(formula="Weight ~ Length2 + Height", data=ryby_df)
res = mod.fit()
# print(res.summary())
# Kvalita modelu se snížila.

# Nakonec pomocí metody target encoding zapracuj do modelu živočišný druh ryby.
prumerna_vaha = ryby_df.groupby('Species')['Weight'].mean()
ryby_df["AverageWeight"] = ryby_df['Species'].map(prumerna_vaha)
print(ryby_df)

mod = smf.ols(formula="Weight ~ Length2 + Height + AverageWeight", data=ryby_df)
res = mod.fit()
print(res.summary())