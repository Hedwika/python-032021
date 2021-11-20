# Zopakuj experiment, ale tentokrát vyber hodnotu parametru n_neighbors na základě metriky precision. Znamená to,
# že pro nás bude důležité, abychom raději označili pitnou vodu za nepitnou, než nepitnou za pitnou. Raději nebudeme
# pít vůbec, než abychom se napili nepitné vody a onemocněli.
#
# V podstatě bude potřeba upravit krok 6. Upravení parametrů modelu. Na základě číselných hodnot nebo grafu vyber tu
# hodnotu parametru, která dává nejlepší výsledek (nejvyšší hodnotu při volání precision()).

import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, precision_score, f1_score, accuracy_score, recall_score
import matplotlib.pyplot as plt

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# 1) Definice problému: Je voda pitná, nebo ne? (dvě možnosti)
r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/water-potability.csv")
open("water-potability.csv", 'wb').write(r.content)
water_potability_df = pd.read_csv("water-potability.csv")

# 2) Data a jejich příprava
water_potability_df = water_potability_df.dropna()
X = water_potability_df.drop(columns=["Potability"])
y = water_potability_df["Potability"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3) a 4) Výběr alforitmu a trénování modelu
clf = KNeighborsClassifier()
clf.fit(X_train, y_train)

# 5. Vyhodnocení modelu
y_pred = clf.predict(X_test)

print(confusion_matrix(y_true=y_test, y_pred=y_pred))

ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
                                      display_labels=clf.classes_,
                                      cmap=plt.cm.Blues)

plt.show()

# 6. Upravení parametrů modelu, nastavení počtu sousedů:
ks = list(range(1, 200))
precision_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    precision_scores.append(precision_score(y_test, y_pred))

precision_scores_sorted = sorted(precision_scores, reverse=True)
high = precision_scores_sorted[0]
print(high)

# 7. závěrečná predikce - výběr n_neighbors založen na nejlepším f1_score
clf = KNeighborsClassifier(n_neighbors=136)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
precision_score(y_test, y_pred)

# 1) Liší se tvůj zvolený parametr od parametru, který jsme jako závěrečný zvolili v lekci?
# Ano
# 2) Jak vypadá matice chyb (confusion matrix)? Dovedeš z matice odvodit výpočet, který nám dá stejnou hodnotu, jako při
# použití metody precision()?
# Ne

# Dobrovolný doplněk
# Vytvoř graf, který bude pro několik parametrů n_neighbors obsahovat všechny čtyři výsledné metriky, které jsme si v
# kurzu ukázali: accuracy, precision, recall, f1_score.
ks = list(range(1, 101))

f1_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1_scores.append(f1_score(y_test, y_pred))

accuracy_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy_scores.append(accuracy_score(y_test, y_pred))

recall_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    recall_scores.append(recall_score(y_test, y_pred))

precision_scores_trim = precision_scores[:100]

plt.plot(ks, f1_scores, label="f1_scores")
plt.plot(ks, precision_scores_trim, label="precision_scores")
plt.plot(ks, recall_scores, label="recall_scores")
plt.plot(ks, accuracy_scores, label="accuracy_scores")
plt.legend()
plt.show()