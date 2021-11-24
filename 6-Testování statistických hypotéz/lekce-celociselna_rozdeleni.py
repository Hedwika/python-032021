import numpy
from scipy.stats import binom
import matplotlib.pyplot as plt
import pandas

n = 10
p = 0.5

# hodíme desetkrát mincí a zajímá nás, kolikrát může padnout líc
data = binom.rvs(n=n, p=p, size=100_000)
plt.hist(data, bins=range(0, n+2), density=True)
plt.show()

# Uvažujme písemnou zkoušku, která má 20 otázek a každá otázka má 4 možné odpovědi, z nichž je právě 1 správná.
# Pomocí binomického rozdělení můžeme snadno spočítat, jaká je pravděpodobnost, že v testu uspějeme tipováním.
# 10 a méně správně zodpovězených otázek = neúspěch
n = 20
p = 0.25

points = list(range(0, 21))
data = binom.cdf(points, n, p)
data = pandas.DataFrame(data)
data["Color"] = numpy.where(data.index > 10, "green", "red")
data[0].plot(kind="bar", color=data["Color"])
plt.show()