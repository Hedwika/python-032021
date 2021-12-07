import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

# Pracuj se souborem auto.csv. Obsahuje informace o vyráběných modelech aut mezi lety 1970-1982.

r = requests.get(
    "https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/auto.csv"
)
open("auto.csv", "wb").write(r.content)

# Načti data. Při volání metody read_csv nastav parametr na_values: na_values=["?"]. Neznámé/prázdné hodnoty jsou totiž
# reprezentované jako znak otazníku. Po načtení dat se zbav řádek, které mají nějakou neznámou/prázdnou hodnotu
# (nápověda: dropna)

auto_df = pd.read_csv("auto.csv", na_values=["?"])
auto_df = auto_df.dropna()
auto_df = auto_df.drop(columns=["name"])
print(auto_df)

# Naše výstupní proměnná bude sloupec "origin". Pod kódy 1, 2 a 3 se skrývají regiony USA, Evropa a Japonsko. Zkus
# odhadnout (třeba pomocí sloupce "name"), který region má který kód :-)
#
# 1 = USA, 2 = Evropa, 3 = Japonsko
#
# Podívej se, jak se měnila spotřeba aut v letech 1970-1982. Vytvoř graf, který ukáže průměrnou spotřebu v jednotlivých
# letech (graf může být sloupcový nebo čarový, a může ukazovat celkovou průměrnou spotřebu, nebo, jako dobrovolný
# doplněk, zobraz spotřebu tak, aby byly rozlišené tři regiony).

auto_pivot = pd.pivot_table(auto_df, values="mpg", index="year", columns="origin", aggfunc=np.mean, margins=True)
auto_pivot = auto_pivot[:-1]
print(auto_pivot)

plt.plot(auto_pivot[1], label="US cars", color="blue")
plt.plot(auto_pivot[2], label="Europe cars", color="green")
plt.plot(auto_pivot[3], label="Japanese cars", color="red")
plt.plot(auto_pivot["All"], label="All cars", color="violet")
plt.xlabel("Years")
plt.ylabel("Mean mpg")
plt.legend(loc='lower right')

# Rozděl data na vstupní a výstupní proměnnou, a následně na trénovací a testovací sadu v poměru 70:30.
X = auto_df.drop(columns=["mpg"])
y = auto_df["mpg"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Data normalizuj
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Použij klasifikační algoritmus rozhodovacího stromu, a vyber jeho parametry technikou GridSearchCV.
model = DecisionTreeClassifier(random_state=42)
tree_para = {'max_depth':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,30,40,50,70,90,120,150], 'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11,12,15,20,30,40,50,70,90,120,150]}

clf = GridSearchCV(model, tree_para, scoring="f1_weighted")
lab_enc = preprocessing.LabelEncoder()
training_scores_encoded = lab_enc.fit_transform(y_train)
clf.fit(X_train, training_scores_encoded)

print(clf.best_params_)

# Jaké jsi dosáhl/a metriky f1_score?
print(round(clf.best_score_, 2))

# Dobrovolný doplněk
# Porovnej DecisionTreeClassifier s aspoň jedním dalším algoritmem, který jsme si ukazovali, například
# KNeighborsClassifier nebo LinearSVC.
model_1 = KNeighborsClassifier()
params_1 = {"n_neighbors": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}

clf_1 = GridSearchCV(model_1, params_1, scoring="f1_weighted")
clf_1.fit(X_train, training_scores_encoded)

print(clf_1.best_params_)
print(round(clf_1.best_score_, 2))

# Zakresli výsledné metriky do sloupcového grafu, ze kterého bude vidět, jak
# si který model podle tebe vede na testovacích datech.
data = {'F1 score': [clf.best_score_, clf_1.best_score_]}

df = pd.DataFrame(data, index=['DecisionTreeClassifier',
                               'KNeighborsClassifier'])

print(df)

df.plot(kind='bar')
plt.show()