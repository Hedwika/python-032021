from scipy.stats import expon
import matplotlib.pyplot as plt

scale = 2

data = expon.rvs(scale=scale, size=100_000)
count, bins, ignored = plt.hist(data, 40, density=True)
plt.plot(bins, expon.pdf(bins, scale=scale), linewidth=1, color='r')
plt.show()