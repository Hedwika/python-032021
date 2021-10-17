# Tabulka crime v naší databázi obsahuje informace o kriminalitě v Chicagu.
# Dataset je poměrně velký, a tak si určitě vytáhneme vždy jen nějaký výběr, se kterým budeme dále pracovat.
#
# 1) Pomocí SQL dotazu si připrav tabulku o krádeži motorových vozidel (sloupec PRIMARY_DESCRIPTION by měl mít hodnotu "MOTOR VEHICLE THEFT").
# 2) Tabulku dále pomocí pandasu vyfiltruj tak, aby obsahovala jen informace o krádeži aut (hodnota "AUTOMOBILE" ve sloupci SECONDARY_DESCRIPTION).
# 3) Ve kterém měsíci dochází nejčastěji ke krádeži auta?