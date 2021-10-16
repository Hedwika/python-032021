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

pocet_obyvatel = pandas.read_sql("pocet_obyvatel", con=engine)
pocet_bytu = pandas.read_sql("pocet_bytu", con=engine)

# SQL dotaz:
# df = pandas.read_sql("SELECT * FROM pocet_obyvatel INNER JOIN pocet_bytu ON pocet_bytu.obec = pocet_obyvatel.obec", con=engine)
# print(df.head())

pocet_obyvatel_a_bytu = pocet_obyvatel.merge(pocet_bytu, how="inner")

def pomer_bytu(radka):
    pomer = 100*radka["pocet_bytu"]/radka["pocet_obyvatel"]
    return pomer

pocet_obyvatel_a_bytu["pomer_bytu"] = pocet_obyvatel_a_bytu.apply(pomer_bytu, axis=1)

pocet_obyvatel_a_bytu_nad_1000 = pocet_obyvatel_a_bytu[pocet_obyvatel_a_bytu["pocet_obyvatel"] > 1000]
pocet_obyvatel_a_bytu_nad_1000 = pocet_obyvatel_a_bytu_nad_1000.sort_values(by="pomer_bytu", ascending=False)

print(pocet_obyvatel_a_bytu_nad_1000.head())