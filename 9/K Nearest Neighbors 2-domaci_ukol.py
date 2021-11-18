import requests

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/kosatce.csv")
open("kosatce.csv", "wb").write(r.content)
# Stáhni si dataset kosatce.csv, který obsahuje pozorování o dvou typech kosatce. Jako vstupní proměnné pro předpověď
# typu kosatce ( Setosa a Virginica) máme délku kalichu a délku okvětního lístku. Výstupní proměnná je označená
# jako target.
#
# Načti si data do proměnných X a y
# Rozděl data na trénovací a testovací (velikost testovacích dat nastav na 30% a nezapomeň nastavit proměnnou
# random_state, aby tvoje výsledky byly reprodukovatelné)
# Pokud použijeme stejný algoritmus jako v prvním úkolu, tj. KNeighborsClassifier, je možné předpovědět typ kosatce
# na základě těchto dat tak, aby metrika f1_score dosáhla alespoň 85%?