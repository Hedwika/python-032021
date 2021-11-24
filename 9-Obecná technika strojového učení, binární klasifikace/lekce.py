import sklearn
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, precision_score, f1_score
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

# zjištění disbalancí mezi hodnotami
print(water_potability_df["Potability"].value_counts(normalize=True))

# Rozdělení na features - sloupce, které určují, zda je pitná, nebo ne
X = water_potability_df.drop(columns=["Potability"])
# a target - cíl který chceme určit
y = water_potability_df["Potability"]

# rozdělení na testovací a trénovací data:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# test_size is the number that defines the size of the test set. It’s very similar to train_size.
# You should provide either train_size or test_size. If neither is given, then the default share of the dataset
# that will be used for testing is 0.25, or 25 percent
# random_state is the object that controls randomization during splitting. It can be either an int or an instance
# of RandomState. The default value is None.

# Standardize features by removing the mean and scaling to unit variance.
scaler = StandardScaler()
# hodnoty jsme se naučili:
X_train = scaler.fit_transform(X_train)
# hodnoty aplikujeme:
X_test = scaler.transform(X_test)

# 3) a 4) Výběr alforitmu a trénování modelu
clf = KNeighborsClassifier()  # model, classifier
clf.fit(X_train, y_train)

# 5. Vyhodnocení modelu
y_pred = clf.predict(X_test)

print(confusion_matrix(y_true=y_test, y_pred=y_pred))

ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
                                      display_labels=clf.classes_,
                                      cmap=plt.cm.Blues)

plt.show()

# True Positives (TP): To jsou data, která jsme označili jako třídu 1, v našem případně za pitnou vodu, a skutečně
# se jednalo o pitnou vodu. Těch máme 97.
# True Negatives (TN): To jsou data, která jsme označili jako třídu 0, v našem případě za nepitnou vodu, a skutečně
# se jednalo o nepitnou vodu. Těch máme 283.
# False Positives (FP): To jsou data, která jsme označili jako třídu 1, ale ve skutečnosti se jednalo o třídu 0.
# O nepitné vodě jsme řekli, že je pitná. Takových případů máme 72.
# False Negatives (FN): To jsou data, která jsme označili jako třídu 0, ale ve skutečnosti se jednalo o třídu 1.
# O pitné vodě jsme řekli, že je nepitná. Takových případů máme 152.`

# Jak teď spočítat úspěšnost modelu? Nabízí se několik metrik:
# Accuracy: Poměr správně určených záznamů oproti celku.
# $A = \frac{TP+TN}{TP+TN+FP+FN}$
# Precision: Tato metrika penalizuje označení nepitné vody za pitnou.
# $P = \frac{TP}{TP+FP}$
# Recall: Tato metrika penalizuje označení pitné vody za nepitnou.
# $R = \frac{TP}{TP+FN}$
# F1 Score: Metrika která zohlední jak Precision, tak Recall.
precision_score(y_test, y_pred)
f1_score(y_test, y_pred)

# 6. Upravení parametrů modelu, nastavení počtu sousedů:
ks = [1, 3, 5, 7, 9]
f1_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)  # model, classifier
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1_scores.append(f1_score(y_test, y_pred))
    print(k, f1_score(y_test, y_pred))

plt.plot(ks, f1_scores)
plt.show()

# 7. závěrečná predikce - výběr n_neighbors založen na nejlepším f1_score
clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
f1_score(y_test, y_pred)