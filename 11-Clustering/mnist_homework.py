from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import numpy as np
import matplotlib.pyplot as plt

# Načti data do proměnné X:
digits = load_digits()
X = digits.data
print(X)

# Data normalizuj
scaler = StandardScaler()
X_reduced = scaler.fit_transform(X)

# Redukuj počet vstupních proměnných na dvě pomocí TSNE. Můžeš vyzkoušet různé parametry.

from sklearn.manifold import TSNE
tsne = TSNE(
    init="pca",
    n_components=2,
    perplexity=10,
    learning_rate="auto",
    random_state=0,
)

X_reduced = tsne.fit_transform(X_reduced)

# Vykresli data do bodového grafu. Kolik odhaduješ shluků (clusterů)?
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], s=10)
plt.show()

# Shluků by mohlo být asi 11 - 15.

# Aplikuj algoritmus KMeans s počtem shluků, který jsi odhadl/a v předchozím kroku
model = KMeans(n_clusters=10, random_state=0)
labels = model.fit_predict(X_reduced)
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=labels, s=10, cmap="Set1")
centers = model.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c="blue", s=100, alpha=0.5)
plt.show()

# Vyhodnoť výsledek pomocí silhouette_score, který by měl být alespoň 0.5
print(silhouette_score(X_reduced, labels))

# Dobrovolný doplněk
# Pokud jsi dosud nepátral/a po původu těchto dat, využij nápovědu níže. O jaký typ dat by se mohlo jednat? Zkus
# nastavovat různé hodnoty proměnné idx, která indexuje řádky původních dat - před redukcí dimenzionality!
# Uměli bychom jednotlivé clustery označit? Podle čeho se data shlukují?
idx = 50
image = np.reshape(X[idx], (8, 8))
plt.imshow(image, cmap="gray_r")
plt.show()

# Vypadá to na nějaké znaky, ale vygooglila jsem, že je to databáze ručně psaných číslic.