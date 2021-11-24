import requests
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/ceny_domu.csv")
# with open("ceny_domu.csv", "wb") as f:
#   f.write(r.content)
#
# r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/insurance.csv")
# with open("insurance.csv", "wb") as f:
#   f.write(r.content)

ceny_domu_df = pd.read_csv("ceny_domu.csv")
print(ceny_domu_df)

mod = smf.ols(formula="prodejni_cena_mil ~ obytna_plocha_m2", data=ceny_domu_df)
# najdi červenou čáru
res = mod.fit()
print(res.summary())

# Modul statsmodels nám pro každou obytnou plochu vypočítal cenu nemovitosti odhadnutou daným modelem. Ty jsou uložené
# v sérii res.fittedvalues. Zobrazíme ji vy grafu červeně a necháme je popojit čarou, aby nám v grafu vznikla přímka.
pred_ols = res.get_prediction()
fig, ax = plt.subplots(figsize=(8, 6))
# modré tečky (b.)
plt.plot(ceny_domu_df["obytna_plocha_m2"], ceny_domu_df["prodejni_cena_mil"], "b.")
# červená čára (r)
plt.plot(ceny_domu_df["obytna_plocha_m2"], res.fittedvalues, "r")
# plt.show()

seaborn.lmplot(x="obytna_plocha_m2", y="prodejni_cena_mil",data=ceny_domu_df)
# plt.show()

# kolik máme chybějících hodnot
print(ceny_domu_df.isna().sum())
# vyplníme je nulou
ceny_domu_df["plocha_pozemku_pred_domem_m2"] = ceny_domu_df["plocha_pozemku_pred_domem_m2"].fillna(0)

# Korelace mezi proměnnými
# Pokud odhalíme korelaci mezi proměnnými, je obvykle lepší přidat do modelu pouze jednu z nich, protože obě proměnné
# jsou nositeli podobné informace. Přidáním obou bychom zbytečně zvýšili kompikovanost modelu, aniž bychom výrazně
# zvýšili jeho přesnost.
seaborn.heatmap(ceny_domu_df.corr(), annot=True, linewidths=.5, fmt=".2f", cmap="Blues", vmax=1)
# plt.show()
# vyřadíme počet aut v garáži (stejnou informaci máme z plochy garáže)
ceny_domu_df = ceny_domu_df.drop("pocet_aut_v_garazi", axis=1)
# U korelační matice je zajímavá i korelace mezi jednotlivými vysvětlujícími a vysvětlovanou proměnnou. Zde je naopak
# podezřelá nízká hodnota, protože to znamená, že tyto proměnné mají slabou lineární závislost. Opět se nabízí možnost
# tyto proměnné z modelu odebrat a tím model zjednodušit bez snížení jeho přesnosti.
ceny_domu_df = ceny_domu_df.drop("plocha_pozemku_pred_domem_m2", axis=1)
ceny_domu_df = ceny_domu_df.drop("plocha_pozemku_m2", axis=1)

# Model s více proměnnými
# Nyní můžeme vytvořit nový model, který bude obsahovat zbývající číselné proměnné.

mod = smf.ols(formula="prodejni_cena_mil ~ obytna_plocha_m2 + celkova_kvalita + rok_vystavby + rok_rekonstrukce "
                      " + plocha_garaze_m2 + pocet_koupelen", data=ceny_domu_df)
res = mod.fit()
print(res.summary())

# Počet koupelen podle našeho modelu snižuje cenu domu. Nedává to smysl, vyřadíme ho.
mod = smf.ols(formula="prodejni_cena_mil ~ obytna_plocha_m2 + celkova_kvalita + rok_vystavby + rok_rekonstrukce "
                      " + plocha_garaze_m2", data=ceny_domu_df)
res = mod.fit()
print(res.summary())

# Výpočet predikce
# Zkusme náš poslední model použít k predikci ceny nějaké nemovitosti.
# Uvažujme nemovitost, která má obythnou plochu 200, hodnocení celkové kvality 8, byla vystavěna v roce 1980
# a rekonstruována v roce 2010 a plocha její garáže je 60.
# Druhé parametry jsou pro druhý dům, můžeme pro oba udělat odhad najednou

data = pd.DataFrame({"obytna_plocha_m2": [200, 150],
                         "celkova_kvalita": [8, 10],
                         "rok_vystavby": [1980, 1990],
                         "rok_rekonstrukce": [2010, 2015],
                         "plocha_garaze_m2": [60, 30]})
print(res.predict(data))

# Nečíselné hodnoty
# print(ceny_domu_df["sousedstvi"].unique())
# print(ceny_domu_df["sousedstvi"].unique().shape)
print(ceny_domu_df.groupby('sousedstvi')['prodejni_cena_mil'].mean().sort_values())

prumery = ceny_domu_df.groupby('sousedstvi')['prodejni_cena_mil'].mean()
ceny_domu_df['sousedstvi_prum_cena'] = ceny_domu_df['sousedstvi'].map(prumery)
predictors = ['plocha_pozemku_pred_domem_m2','plocha_pozemku_m2', 'obytna_plocha_m2', 'celkova_kvalita','rok_vystavby',
              'rok_rekonstrukce','plocha_garaze_m2','sousedstvi_prum_cena']

print(ceny_domu_df)

mod = smf.ols(formula="prodejni_cena_mil ~ obytna_plocha_m2 + celkova_kvalita + rok_vystavby + rok_rekonstrukce "
                      " + plocha_garaze_m2 + sousedstvi_prum_cena", data=ceny_domu_df)
res = mod.fit()
print(res.summary())

data = pd.DataFrame({"obytna_plocha_m2": [200, 150],
                         "celkova_kvalita": [8, 10],
                         "rok_vystavby": [1980, 1990],
                         "rok_rekonstrukce": [2010, 2015],
                         "plocha_garaze_m2": [60, 30],
                     "sousedstvi_prum_cena": [1, 5]})
print(res.predict(data))