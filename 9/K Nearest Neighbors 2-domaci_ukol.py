import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, f1_score
import matplotlib.pyplot as plt

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/kosatce.csv")
open("kosatce.csv", "wb").write(r.content)
# Stáhni si dataset kosatce.csv, který obsahuje pozorování o dvou typech kosatce. Jako vstupní proměnné pro předpověď
# typu kosatce (Setosa a Virginica) máme délku kalichu a délku okvětního lístku. Výstupní proměnná je označená
# jako target.

kosatce_df = pd.read_csv("kosatce.csv")
print(kosatce_df)

# Načti si data do proměnných X a y
X = kosatce_df.drop(columns=["target"])
y = kosatce_df["target"]

# Rozděl data na trénovací a testovací (velikost testovacích dat nastav na 30% a nezapomeň nastavit proměnnou
# random_state, aby tvoje výsledky byly reprodukovatelné)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Pokud použijeme stejný algoritmus jako v prvním úkolu, tj. KNeighborsClassifier, je možné předpovědět typ kosatce
# na základě těchto dat tak, aby metrika f1_score dosáhla alespoň 85%?
# Ano
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

clf = KNeighborsClassifier()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(confusion_matrix(y_true=y_test, y_pred=y_pred))

ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
                                      display_labels=clf.classes_,
                                      cmap=plt.cm.Blues)

plt.show()

ks = list(range(1, 31))
f1_scores = []

for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1_scores.append(f1_score(y_test, y_pred))

f1_scores_sorted = sorted(f1_scores, reverse=True)
high = f1_scores_sorted[0]
print(high)