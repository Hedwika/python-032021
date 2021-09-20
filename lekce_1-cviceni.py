import numpy
import pandas as pd
import requests

# Pracuješ pro společnost, která spustila ve dvou vybraných zemích (České republice a Rakousku) službu na dovoz jídla z restaurací. Spuštění služby bylo doprovázeno intenzivní marketingovou kampaní, která obsahovala reklamu v tisku, televizi, billboardy, reklamu na sociálních sítích a slevám za doporučení nového uživatele.
#
# Data k úkolu najdeš v souboru excs_data/user_registrations.json.
#
# Tvým úkolem je vyhodnotit výsledky spuštění služby v obou zemích. V souboru jsou záznamy o registracích uživatelů: email uživatele, adresa, odkud se o službě dozvěděli, věková skupina.

# Služba vyžaduje ověření e-mailu. Pokud e-mail není ověřen do 24 hodin, musí se uživatel zaregistrovat znovu. Tím vzniká záznam o registraci s duplicitní e-mailovou adresou. Očisti tedy soubor o tyto duplicity.
r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/user_registration.json")
open("user_registration.json", 'wb').write(r.content)

df_users = pd.read_json("user_registration.json")
# print(df_users.columns)
# print(df_users)
df_users = df_users.drop_duplicates(subset="email", keep="last")
# print(df_users)

# Pomocí kontingenční tabulky porovnej věkovou skupinu uživatelů a to, jak se o službě dozvěděli. Výsledky prezentuj pomocí teplotní mapy.
df_users_for_pivot = df_users.drop(columns=['date_time', 'email', 'ip_address'])
pd.options.display.max_columns = None
df_users_pivot = pd.pivot_table(df_users_for_pivot, index="age_group", columns="marketing_channel", aggfunc=numpy.count_nonzero, margins=True)
print(df_users_pivot)

# Proveď agregaci dle data a pomocí kumulativního součtu urči, jak rychle rostl počet uživatelů služby během prvního měsíce.
df_users["date_time"] = pd.to_datetime(df_users["date_time"]).dt.date
df_users = df_users.groupby(["date_time"])["ip_address"].count()
print(df_users.cumsum())