import requests
import pandas as pd
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/titanic.csv")
open("titanic.csv", 'wb').write(r.content)

# V souboru titanic.csv najdeš informace o cestujících na zaoceánském parníku Titanic.
# Vytvoř kontingenční tabulku, která porovná závislost mezi pohlavím cestujícího (soupec Sex), třídou (sloupec Pclass),
# ve které cestoval, a tím, jesti přežil potopení Titanicu (sloupec Survived).
# Pro data můžeš použít agregaci numpy.sum, která ti spočte absolutní počet přeživších pro danou kombinaci,
# nebo numpy.mean, která udá relativní počet přeživších pro danou kombinaci.

titanic = pd.read_csv("titanic.csv")

titanic_aggregated_sum = titanic.groupby(["Sex", "Pclass"])["Survived"].sum()
titanic_aggregated_sum = pd.DataFrame(titanic_aggregated_sum)
print("Absolutní počet přeživších potopení Titanicu v závislosti na pohlaví a třídě, ve které cestovali:")
print(titanic_aggregated_sum)

titanic_aggregated_mean = titanic.groupby(["Sex", "Pclass"])["Survived"].mean()
titanic_aggregated_mean = pd.DataFrame(titanic_aggregated_mean)
print("Relativní počet přeživších potopení Titanicu v závislosti na pohlaví a třídě, ve které cestovali:")
print(titanic_aggregated_mean)

# Rozšířené zadání¶
# Rozšířená zadání jsou čistě pro dobrovolníky, kteří mají hodně času a hledají větší výzvu :-)
# Z dat vyfiltruj pouze cestující, kteří cestovali v první třídě.
# Dále použij metodu cut na rozdělení cestujících do věkových skupin (zkus vytvořit např. 4 skupiny, můžeš definovat
# hranice skupin tak, aby vznikly skupiny děti, teenageři, dospělí a senioři). Urči relativní počet přeživších
# pro jednotlivé kombinace pohlaví a věkové skupiny.
titanic["age_group"] = pd.cut(titanic["Age"], bins=[0, 12, 19, 65, 120])
titanic_first_class = titanic[titanic.Pclass < 2]
titanic_first_class_survivors = titanic_first_class.groupby(["Sex", "age_group"])["Survived"].mean()
titanic_first_class_survivors = pd.DataFrame(titanic_first_class_survivors)
print("Relativní počet přeživších potopení Titanicu v první třídě, rozdělení do věkových kategorií:")
print(titanic_first_class_survivors)