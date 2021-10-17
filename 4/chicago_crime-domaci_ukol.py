import pandas as pd
from sqlalchemy import create_engine

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

# Tabulka crime v naší databázi obsahuje informace o kriminalitě v Chicagu.
# Dataset je poměrně velký, a tak si určitě vytáhneme vždy jen nějaký výběr, se kterým budeme dále pracovat.
HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "pajerova.hedvika"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "fRlFJSsmEtbewIvX"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)
crime = pd.read_sql(f"crime", con=engine)

# 1) Pomocí SQL dotazu si připrav tabulku o krádeži motorových vozidel
# (sloupec PRIMARY_DESCRIPTION by měl mít hodnotu "MOTOR VEHICLE THEFT").
motor_vehicle_theft = pd.read_sql("SELECT * from crime WHERE \"PRIMARY_DESCRIPTION\" = 'MOTOR VEHICLE THEFT'", con=engine)
motor_vehicle_theft = pd.DataFrame(motor_vehicle_theft)

# 2) Tabulku dále pomocí pandasu vyfiltruj tak, aby obsahovala jen informace o krádeži aut
# (hodnota "AUTOMOBILE" ve sloupci SECONDARY_DESCRIPTION).
motor_vehicle_theft = motor_vehicle_theft.loc[motor_vehicle_theft["SECONDARY_DESCRIPTION"] == "AUTOMOBILE"]

# 3) Ve kterém měsíci dochází nejčastěji ke krádeži auta?
motor_vehicle_theft["date"] = pd.to_datetime(motor_vehicle_theft["DATE_OF_OCCURRENCE"])
motor_vehicle_theft["month"] = motor_vehicle_theft["date"].dt.month
motor_vehicle_theft_months = pd.DataFrame(motor_vehicle_theft)
motor_vehicle_theft_months_only = motor_vehicle_theft_months.groupby(["month"])["BLOCK"].count()
motor_vehicle_theft_months_only = motor_vehicle_theft_months_only.sort_values(ascending=False)
print(motor_vehicle_theft_months_only.head())
