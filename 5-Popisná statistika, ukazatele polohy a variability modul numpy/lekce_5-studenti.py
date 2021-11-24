import statistics
import matplotlib.pyplot as plt

student_research_age = [
  18,
  17,
  15,
  15,
  16,
  16,
  16,
  17,
  15,
  15,
  15,
  15,
  15,
  15,
  15,
  16,
  16,
  16,
  17,
  16
]

# Modus (představuje hodnotu, která se v daném souboru vyskytuje nejčastěji):
print(statistics.mode(student_research_age))

student_research_age_gender = [
  ("F", 18),
  ("F", 17),
  ("F", 15),
  ("F", 15),
  ("F", 16),
  ("M", 16),
  ("M", 16),
  ("F", 17),
  ("M", 15),
  ("M", 15),
  ("F", 15),
  ("F", 15),
  ("M", 15),
  ("M", 15),
  ("M", 15),
  ("F", 16),
  ("F", 16),
  ("F", 16),
  ("M", 17),
  ("M", 16),
  ("M", 15),
]

print(statistics.mode(student_research_age_gender))


# Dvojice hodnot jsou zde uložené ve struktuře, které říkáme tuple. Ta funguje podobně jako seznam,
# oproti němu však po vytvoření není možné hodnoty v tuple měnit. Neexistují pro něj tedy například metody append
# nebo pop. Neměnnost tuple umožňuje vypočítat tvz. hash, což je jakýsi otisk.
# Python tedy neporovnává přímo hodnoty v tuple, ale jejich vypočítané hash
print(student_research_age_gender[0].__hash__())
print(student_research_age_gender[2].__hash__())
print(student_research_age_gender[3].__hash__())