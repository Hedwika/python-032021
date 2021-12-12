# Feature Importance
# Pracuj se stejnými daty jako na cvičení, tj. se souborem soybean-2-rot.csv. Rozhodovací strom nám umožňuje nahlédnout
# do pravidel, podle kterých postupuje v klasifikaci. Díky tomu se často pokládá za velice průhledný nebo dobře
# interpretovatelný algoritmus.

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
import requests
from sklearn.datasets import load_iris

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# r = requests.get(
#     "https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/soybean-2-rot.csv"
# )
# open("soybean-2-rot.csv", "wb").write(r.content)

data = pd.read_csv("soybean-2-rot.csv")
print(data.head())

X = data.drop(columns=["class"])
y = data["class"]

oh_encoder = OneHotEncoder()
X = oh_encoder.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0
)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1, random_state=0)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average="weighted"))

# Podívej se na atribut featureimportances (clf.featureimportances), který říká, které vstupní proměnné model použil
# pro rozhodování. Některé budou mít nulovou hodnotu, to znamená, že vůbec potřeba nejsou. Atribut nám dá jen seznam
# čísel seřazený podle vstupních proměnných, ale ne jejich jména. Ty získáš například z OneHotEncoder (atribut
# feature_namesin, takže například níže by se jednalo o oh_encoder.feature_namesin)
feature_names = oh_encoder.get_feature_names()

def print_feature_importance(names_array, importances_array):
    """ Prints out a feature importance array as a dataframe. """
    importances = pd.DataFrame(data=names_array)
    importances[1] = importances_array
    importances = importances.T
    importances.drop(0, axis=0, inplace=True)
    importances.columns = feature_names

    print(str(importances.reset_index(drop=True)))

print_feature_importance(feature_names, clf.feature_importances_)

# Která vstupní proměnná má největší "důležitost"?
features = oh_encoder.get_feature_names()[0]
print(features)

# Stačí nám tato proměnná pro úspěšnou klasifikaci? Jaký je rozdíl mezi hodnotou f1_score při použití všech proměnných
# a jen této jedné "nejdůležitější" proměnné?

X = data["plant-stand"]
y = data["class"]

oh_encoder = OneHotEncoder()
X = oh_encoder.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0
)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1, random_state=0)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average="weighted"))

# Dobrovolný doplněk
# Vykresli graf, ze kterého je vidět rozložení hodnot této jedné nejdůležitější proměnné. Můžeš využít groupby nebo
# pivot_table v kombinaci s metodou plot, nebo například sns.countplot (kde sns je modul seaborn).
