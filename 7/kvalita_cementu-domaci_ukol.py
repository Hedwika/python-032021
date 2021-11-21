import requests
import pandas as pd
import statsmodels.formula.api as smf

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# V souboru Concrete_Data_Yeh.csv najdeš informace o kvalitě cementu.
#
# Sloupce 1-7 udávají množství jednotlivých složek v kg, které byly přimíchány do krychlového metru betonu
# (např. cement, voda, kamenivo, písek atd.). Ve sloupci 8 je stáří betonu a ve sloupci 9 kompresní síla betonu
# v megapascalech.
r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Concrete_Data_Yeh.csv")
with open("Concrete_Data_Yeh.csv", "wb") as f:
  f.write(r.content)
cement_kvalita_df = pd.read_csv("Concrete_Data_Yeh.csv")
print(cement_kvalita_df)

# Vytvoř regresní model, který bude predikovat kompresní sílu betonu na základě všech množství jednotlivých složek
# a jeho stáří.
mod = smf.ols(formula="csMPa ~ cement + slag + flyash + water + superplasticizer + coarseaggregate + fineaggregate"
                      " + age", data=cement_kvalita_df)
res = mod.fit()
print(res.summary())

# Zhodnoť kvalitu modelu.
# Dobré, ale mohlo by to být lepší :)

# Tipni si, která ze složek betonu ovlivňuje sílu betonu negativní (tj. má záporný regresní koeficient). Napiš,
# o kterou složku jde, do komentáře svého programu.
# Jedná se o složku voda s daty ve sloupci water.