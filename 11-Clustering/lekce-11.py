import pandas
import requests

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples

desired_width = 1000
pandas.set_option('display.width', desired_width)
pandas.set_option('display.max_columns',100)

# datasets_url = (
#     "https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets"
# )
#
# r = requests.get(f"{datasets_url}/wine-quality.csv")
# open("wine-quality.csv", "wb").write(r.content)
# r = requests.get(f"{datasets_url}/wine-quality-targets.csv")
# open("wine-quality-targets.csv", "wb").write(r.content)
#
# r = requests.get(f"{datasets_url}/wine-regions.csv")
# open("wine-regions.csv", "wb").write(r.content)
# r = requests.get(f"{datasets_url}/wine-regions-targets.csv")
# open("wine-regions-targets.csv", "wb").write(r.content)

X = pandas.read_csv("wine-quality.csv")
print(X.head())

# normalizace dat
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Vizualizace by byla fajn, ale nelze vizualizovat 11 proměnných. Snížíme tedy jejich počet.
# Jedna z metod, která nám sníží počet proměnných ("redukuje dimenzionalitu") se jmenuje t-SNE
# (t-distributed Stochastic Neighbor Embedding).
tsne = TSNE(
    # init označuje metodu inicializace. Obecně se předpokládá, že pokud chceme zachovat vztahy mezi datovými body
    # (ty které si byly blízké v našich mnoha dimenzích si jsou stále blízké v méně dimenzích),
    # je dobré zvolit metodu "pca".
    init="pca",
    # počet výsledných proměnných, u t-SNE typicky volíme hodnotu 2 nebo 3.
    n_components=2,
    # perplexity určuje, podle kolika sousedů se má metoda t-SNE řídit. Čím vyšší je náš dataset, tím vyšší hodnotu
    # parametru nastavíme. Běžně se používají hodnoty mezi 5 a 50.
    perplexity=10,
    # learning_rate označuje velikost učícího kroku - k výsledku se t-SNE dopracovává iterativně, a s velkou hodnotou
    # learning rate postupuje sice rychle, ale může optimální výsledek "přeskočit", s malou hodnotou postupuje pečlivěji,
    # ale může zase skončit v nějakém neoptimálním stavu. Vyzkoušejte si, jaký vliv má tento parametr na zobrazení
    # vašich dat tak, že postupně nastavíte velmi malé (kolem 10) i velmi vysoké hodnoty (kolem 1000). Pro naše účely
    # necháme TSNE ať nám tento parametr nastaví za nás.
    learning_rate="auto",
    random_state=0,
)
X = tsne.fit_transform(X)
# print(X.shape)

plt.scatter(X[:, 0], X[:, 1], s=50)
plt.show()

# můžeme spustit algorytmus K-means
model = KMeans(n_clusters=2, random_state=0)
labels = model.fit_predict(X)

plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap="Set1")
centers = model.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c="black", s=200, alpha=0.5)
plt.show()

# Vyhodnocení úspěšnosti clusterovacího algoritmu
# Silhouette koeficient bere v úvahu průměrnou vzdálenost mezi bodem a všemi body, které jsou ve stejném shluku,
# a pak vzdálenost mezi bodem a všemi body v nejbližším jiném shluku. Jeho hodnota se nachází mezi 1 a -1.
# Čím vyšší je tento koeficient, tím lépe definované jsou clustery (body se nachází blízko svému shluku a daleko
# od všech ostatních). Pokud má hodnotu kolem nuly, značí to, že se naše shluky překrývají (existují body na rozhraní
# dvou shluků).
print(silhouette_score(X, labels))

# Můžeme si vykreslit toto skóre pro každý bod clusteru.
# Podle
# https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py
n_clusters = model.n_clusters

fig, ax = plt.subplots(figsize=(15, 8))

silhouette_avg = silhouette_score(X, labels)
print(
    "For n_clusters =",
    n_clusters,
    "The average silhouette_score is :",
    silhouette_avg,
)

# Compute the silhouette scores for each sample
sample_silhouette_values = silhouette_samples(X, labels)

y_lower = 10
for i in range(n_clusters):
    # Aggregate the silhouette scores for samples belonging to
    # cluster i, and sort them
    ith_cluster_silhouette_values = sample_silhouette_values[labels == i]

    ith_cluster_silhouette_values.sort()

    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = cm.nipy_spectral(float(i) / n_clusters)
    ax.fill_betweenx(
        np.arange(y_lower, y_upper),
        0,
        ith_cluster_silhouette_values,
        facecolor=color,
        edgecolor=color,
        alpha=0.7,
    )

    # Label the silhouette plots with their cluster numbers at the middle
    ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    y_lower = y_upper + 10  # 10 for the 0 samples

ax.axvline(x=silhouette_avg, color="red", linestyle="--")
plt.show()

# Měli bychom se vyvarovat situace, kdy celý jeden cluster je pod průměrným silhouette koeficientem (tj. nalevo od
# červené čáry), dále můžeme pozorovat velikost jednotlivých clusterů (výška barevné sekce) a jestli nejsou rozdíly
# mezi barevnými sekcemi příliš velké co se týče šířky (hodnota koeficientu pro jednotlivé body).

# Na závěr si pojďme vizuálně zobrazit naše shluky podle skutečných hodnot
y = pandas.read_csv("wine-quality-targets.csv")
y = y["quality"]
plt.figure(figsize=(15, 5))

# sp1
plt.subplot(121)
scatter = plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap="cool", alpha=0.8)
centers = model.cluster_centers_
plt.legend(handles=scatter.legend_elements()[0], labels=list(y.unique()))
plt.show()

# sp2
plt.subplot(122)
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap="Set1")
centers = model.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c="black", s=200, alpha=0.5)
plt.show()