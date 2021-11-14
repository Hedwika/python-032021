import statistics
import requests
import seaborn
import pandas as pd
import matplotlib.pyplot as plt

desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',100)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/UberDrives.csv")
open("UberDrives.csv", "wb").write(r.content)
uber_drives = pd.read_csv("UberDrives.csv")
print(uber_drives)

# Nahraj si data ze souboru UberDrives.csv a spočítej a interpretuj následující statistiky:
# Pro ujetou vzdálenost (sloupec MILES) urči průměr, medián, rozptyl a varianční rozpětí podle typu jízdy (sloupec CATEGORY).
print(statistics.mean(uber_drives["MILES"]))
print(statistics.median(uber_drives["MILES"]))
print(statistics.pvariance(uber_drives["MILES"]))
print(max(uber_drives["MILES"]) - min(uber_drives["MILES"]))

# Vypočti délku jízdy (rozdíl časových údajů ve sloupcích END_DATE a START_DATE) v minutách nebo hodinách.
uber_drives["start_date_converted"] = pd.to_datetime(uber_drives["START_DATE"])
uber_drives["START_DATE"] = uber_drives["start_date_converted"].dt.date
uber_drives["START_hour"] = uber_drives["start_date_converted"].dt.hour
uber_drives["START_sec"] = uber_drives["start_date_converted"].dt.minute
uber_drives["START_SECONDS"] = (uber_drives["START_hour"]*60 + uber_drives["START_sec"])

uber_drives["end_date_converted"] = pd.to_datetime(uber_drives["END_DATE"])
uber_drives["END_DATE"] = uber_drives["end_date_converted"].dt.date
uber_drives["END_hour"] = uber_drives["end_date_converted"].dt.hour
uber_drives["END_sec"] = uber_drives["end_date_converted"].dt.minute
uber_drives["END_SECONDS"] = (uber_drives["END_hour"]*60 + uber_drives["END_sec"])

uber_drives["ride_lenght"] = uber_drives["END_SECONDS"] - uber_drives["START_SECONDS"]
print(uber_drives)

# Zjisti, jaká je korelace mezi délkou jízdy a vzdáleností.
legth_miles = uber_drives.drop(columns=['START_DATE', 'END_DATE', 'CATEGORY', 'START', 'STOP', 'PURPOSE',
                                        'start_date_converted', 'START_hour', 'START_sec', 'START_SECONDS',
                                        'end_date_converted', 'END_hour', 'END_sec', 'END_SECONDS'])

seaborn.jointplot("MILES", "ride_lenght", legth_miles, kind='scatter', color='seagreen')
plt.show()