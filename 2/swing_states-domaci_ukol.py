import requests
import pandas as pd
import numpy as np

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/1976-2020-president.csv") as r:
#   open("1976-2020-president.csv", 'w', encoding="utf-8").write(r.text)

swing_states = pd.read_csv("1976-2020-president.csv")

# V případě amerických prezidentských voleb obecně platí, že ve většině států dlouhodobě vyhrávají kandidáti jedné strany.
# Například v Kalifornii vyhrává kandidát Demokratické strany or roku 1992, v Texasu kandidát Republikánské strany
# od roku 1980, v Kansasu do konce od roku 1968 atd. Státy, kde se vítězné strany střídají, jsou označovány jako
# "swing states" ("kolísavé státy"). Tvým úkolem je vybrat státy, které lze označit jako swing states.
# V souboru 1976-2020-president.csv najdeš historické výsledky amerických prezidentských voleb.
# Každý řádek souboru obsahuje počet hlasů pro kandidáta dané strany v daném roce.
# V souboru jsou důležité následující sloupce:
# Year - rok voleb,
# State - stát,
# party_simplified - zjednodušené označení politické strany,
# candidatevotes - počet hlasů pro vybraného kandidáta,
# totalvotes - celkový počet odevzdaných hlasů.

# Proveď níže uvedené úkoly.
# 1) Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech
# (pomocí metody rank()). Nezapomeň, že data je před použitím metody nutné seřadit a spolu
# s metodou rank() je nutné použít metodu groupby().
swing_states["Rank"] = swing_states.groupby(["year", "state"])["candidatevotes"].rank(method="min", ascending=False)

# 2) Pro další analýzu jsou důležití pouze vítězové. Ponech si v tabulce pouze řádky, které obsahují vítěze voleb
# v jednotlivých letech v jednotlivých státech.
swing_states = swing_states[swing_states["Rank"] == 1.0]

# 3) Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a) po sobě vítězné strany ve dvou
# po sobě jdoucích letech.
swing_states = swing_states.sort_values(["state", "year"])
swing_states["last_voting_winning_party"] = swing_states["party_simplified"].shift(periods=+1)

# 4) Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana. Můžeš k tomu použít např.
# funkce numpy.where a vložit hodnotu 0 nebo 1 podle toho, jestli došlo ke změně vítězné strany.
swing_states = swing_states.dropna(axis=0, subset=['last_voting_winning_party']).reset_index(drop=True)
swing_states["changes"] = np.where(swing_states["party_simplified"] == swing_states["last_voting_winning_party"], 0, 1)

# 5) Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.
swing_states_sum = pd.DataFrame(swing_states.groupby(["state"])["changes"].sum())
swing_states_sum["ranking"] = swing_states_sum["changes"].rank(method="min", ascending=True)
swing_states_sum = swing_states_sum.sort_values(["ranking"])
# print("Počet změn vítězných stran (changes) je od roku 1980 v amerických státech následující:")
# print(swing_states_sum)

# Dobrovolný doplněk
# U amerických voleb je zajímavý i tzv. margin, tedy rozdíl mezi prvním a druhým kandidátem.
# 1) Přidej do tabulky sloupec, který obsahuje absolutní rozdíl mezi vítězem a druhým v pořadí.
# Nezapomeň, že je k tomu potřeba kompletní dataset, tj. je potřeba tabulku znovu načíst, protože v předchozí části
# jsme odebrali některé řádky.
swing_states_margin = pd.read_csv("1976-2020-president.csv")
swing_states_margin["Rank"] = swing_states_margin.groupby(["year", "state"])["candidatevotes"].rank(method="min", ascending=False)
!!! swing_states_margin = swing_states_margin[(swing_states_margin["Rank"] == 1.0) or (swing_states_margin["Rank"] == 2.0)]
print(swing_states_margin.head())

!!! swing_states_margin["1st_runner"] = swing_states_margin["candidatevotes"].shift(periods=-1)
!!! swing_states_margin = swing_states_margin[swing_states_margin["Rank"] == 1.0]
!!! swing_states_margin["Difference"] = swing_states_margin["candidatevotes"] - swing_states_margin["Differnce"]

# 2) Můžeš přidat i sloupec s relativním marginem, tj. rozdílem vyděleným počtem hlasů.
!!! swing_states_margin["Relative_difference"] = swing_states_margin["Difference"] / swing_states_margin["totalvotes"]

# 3) Seřaď tabulku podle velikosti margin (absolutním i relativním) a zjisti, kde byl výsledek voleb nejtěsnější.
!!! swing_states_margin = swing_states_margin.sort_values(["Relative_difference", "Difference"], ascending=True)