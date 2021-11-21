import requests
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/insurance.csv")
with open("insurance.csv", "wb") as f:
  f.write(r.content)

insurance_df = pd.read_csv("insurance.csv")
print(insurance_df)

# V souboru insurance.csv najdeš informace o pojištěncích u zdravotní pojišťovny. Pro každého pojištěnce máš
# následující informace:
#
# věk (sloupec age),
# pohlaví (sloupec sex),
# BMI (sloupec bmi),
# počet dětí (sloupec children),
# zda je pojištěnec kuřák (sloupec smoker),
# celkokvé požadavky pojištěnce k pojišťovně (sloupec charges).
#
# Sestav regresní model, který bude na základě věku a pohlaví počítat výši pojistných nároků. Rozhodni o kvalitě takto
# sestaveného modelu.
insurance_df["sex"] = pd.get_dummies(insurance_df.sex).male

mod = smf.ols(formula="charges ~ age + sex", data=insurance_df)
res = mod.fit()
print(res.summary())

# Přidej do modelu informace o tom, zda je pojištěnec kuřák. Zhodnoť, nakolik se tím zvýšila kvalita modelu.
insurance_df["smoker"] = insurance_df["smoker"].replace
insurance_df["smoker"] = pd.get_dummies(insurance_df.smoker)."True"
print(insurance_df)

# Nakonec přidej do modelu informaci o regionu. Použij metodu target encoding, kterou jsme si ukazovali během lekce.