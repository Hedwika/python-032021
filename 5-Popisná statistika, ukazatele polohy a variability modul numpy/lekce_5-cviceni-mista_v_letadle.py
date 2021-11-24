# Uvažuj, že v našem dopravním letadle je 47 řad a každá z nich má 6 sedadel, které jsou označené písmeny A až F.
# Pomocí funkce itertools.product vygeneruj seznam všech míst, která jsou v letadle.
# Pro vytvoření seznamu čísel od 1 do 47 zkus použít funkci range().

import itertools
rows = range(1, 48)
seats = ("A", "B", "C", "D", "E", "F")

list_of_seats = list(itertools.product(rows, seats))

for item in list_of_seats:
  print(f"{item[0]} {item[1]}")