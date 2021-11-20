import os
import pandas
import psycopg2
from sqlalchemy import create_engine, inspect

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "pajerova.hedvika"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "fRlFJSsmEtbewIvX"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)

# Databáze v mezipaměti:
# engine = create_engine("sqlite:///:memory:")
# Databáze s uložením:
# engine= create_engine("sqlite:///databaze.db")

# inspector = inspect(engine)
# print(inspector.get_table_names())

# Nahrání tabulky z databáze:
df = pandas.read_sql(f"uzivatele-{USER}", con=engine)
print(df)

# SQL dotaz:
# df = pandas.read_sql("SELECT address_street, country from \"uzivatele-pajerova.hedvika\" WHERE produkt = 'sušička ovoce'", con=engine)
# Klasický pandas dotaz:
# print(df[df["produkt"] == "sušička ovoce"]["address_street", "country"])

# Nastavení cen produktů:
def cena_produktu(radka):
    ceny = {"kávovar": 2000, "šicí stroj": 5000, "topinkovač": 600, "sušička ovoce": 3000}
    produkt = radka["produkt"]
    # None = neznámá cena, lze použít i číslo, co se přiřadí defaultně, například 0
    return ceny.get(produkt, None)

df["cena"]= df.apply(cena_produktu, axis=1)

# Uložení df zpět do databáze
# df.to_sql(f"uzivatele-{USER}", con=engine, index=False, if_exists="replace")

# Vytvoření nového dataframu a přidání ke stávajícímu do databáze:
nova_data = pandas.DataFrame({"name": ["Hana", "Andrea"], "country": ["Czech Republic", "Czech Republic"],
                              "address_street": ["Korunní", "Vinohradská"], "age":[35, 45], "produkt": ["kávovar", "vysavač"]})
nova_data.to_sql(f"uzivatele-{USER}", con=engine, index=False, if_exists="append")

df = pandas.read_sql(f"uzivatele-{USER}", con=engine)
print(df)