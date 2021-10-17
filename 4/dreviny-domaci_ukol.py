import pandas as pd
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# Tabulka dreviny v naší databázi obsahuje informace o těžbě dřeva podle druhů dřevin a typu těžby.
# Objem těžby se nachází ve sloupci hodnota.

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "pajerova.hedvika"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "fRlFJSsmEtbewIvX"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)

dreviny = pd.read_sql(f"dreviny", con=engine)

# 1) Pomocí SQL dotazu do databáze si připrav dvě pandas tabulky:
# - tabulka smrk bude obsahovat řádky, které mají v sloupci dd_txt hodnotu "Smrk, jedle, douglaska"
smrk = pd.read_sql("SELECT * from dreviny WHERE dd_txt = 'Smrk, jedle, douglaska'", con=engine)
smrk = pd.DataFrame(smrk)

# - tabulka nahodila_tezba bude obsahovat řádky, které mají v sloupci druhtez_txt hodnotu "Nahodilá těžba dřeva"
nahodila_tezba = pd.read_sql("SELECT * from dreviny WHERE druhtez_txt = 'Nahodilá těžba dřeva'", con=engine)
nahodila_tezba = pd.DataFrame(nahodila_tezba)

# 2) Vytvoř graf, který ukáže vývoj objemu těžby pro tabulku smrk. Pozor, řádky nemusí být seřazené podle roku.
smrk_objem_tezby = smrk.groupby(["rok"]).sum()
smrk_objem_tezby.plot(kind="bar", y=["hodnota"], title="Vývoj těžby smrku v letech 2000 - 2020", legend=True)
plt.show()

# 3) Vytvoř graf, který ukáže vývoj objemu těžby pro různé typy nahodilé těžby: Agreguj tabulku nahodila_tezba
# podle sloupce prictez_txt a na výsledek operace groupby zavolej metodu plot s parametrem legend=True.
nahodila_tezba_typy = nahodila_tezba.groupby(["prictez_txt"]).sum()
print(nahodila_tezba_typy)
nahodila_tezba_typy.plot(kind="bar", y=["hodnota"], title="Příčina nahodilé těžby", legend=True)
plt.show()