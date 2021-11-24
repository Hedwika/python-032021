from scipy.stats import norm
import matplotlib.pyplot as plt

mu = 100
sigma = 15

# size = kolik dat chci generovat, scale = směrodatná odchylka, loc = data, co mají průměr mu
data = norm.rvs(loc=mu, scale=sigma, size=100_000)
# plt.hist(data, 30, density=True)
# plt.show()
# plt.hist(data, bins=200)
# plt.show()

count, bins, ignored = plt.hist(data, bins=100, density=True)
# červená čára = funkce hustoty.
# Pokud si vybereme dvě hodnoty, plocha pod funkcí hustoty nám řekne, kolik procent všech hodnot v nějakém souboru
# se nachází v daném intervalu.
plt.plot(bins, norm.pdf(bins, mu, sigma), color="red")
# plt.show()

# 178 = to, co chceme zjistit. Kolik % mužů má výšku do 178 cm? 180 = průměrná výška mužů, 8 = směrodatná odchylka
mensi_nez_178 = norm.cdf(178, 180, 8)
mensi_nez_186 = norm.cdf(186, 180, 8)
rozdil = mensi_nez_186 - mensi_nez_178
# print(rozdil)