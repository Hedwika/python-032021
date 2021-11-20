import statistics
import matplotlib.pyplot as plt

first_seven_days = [
  5.1,
  5,
  4.8,
  4.7,
  63.7,
  4.3,
  7.1,
  0.8,
]


# x = range(1, len(first_seven_days) + 1)
# plt.bar(x, first_seven_days)
# plt.show()

# Aritmetický průměr:
# print(statistics.mean(first_seven_days))

# Medián (hodnota uprostřed seznamu, pokud hodnoty seřadíme od nejmenší po největší):
# print(statistics.median(first_seven_days))

second_seven_days = [
  8.3,
  16.5,
  10.8,
  7.5,
  6.2,
  6.4,
  1.6,
  1.7,
  1.9,
  1.9,
  4,
  1.8,
  2.4,
  2,
  15.1,
  11.2,
  11.8,
  21.9,
  3.9
]

# Rozptyl (udává, jak moc jsou hodnoty v našem statistickém soubory rozptýleny):
print(statistics.pvariance(first_seven_days))
print(statistics.pvariance(second_seven_days))

# Směrodatná odchylka (podobně jako rozptyl, určuje jako moc jsou hodnoty rozptýleny či odchýleny od průměru hodnot. Je to odmocnina rozptylu):
print(statistics.pstdev(first_seven_days))
print(statistics.pstdev(second_seven_days))

# varianční rozpětí:
print(max(first_seven_days) - min(first_seven_days))
print(max(second_seven_days) - min(second_seven_days))

x = range(1, len(second_seven_days) + 1)
plt.bar(x, second_seven_days)
plt.show()