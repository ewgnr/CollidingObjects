import numpy as np
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

data = np.array([
    [1, 2, 3, 4, 5, 10],
    [1, 2, 3, 4, 5, 12],
    [1, 3, 2, 4, 6, 11],
    [7, 8, 9, 10, 11, 15],
    [8, 7, 10, 11, 12, 16],
    [30, 40, 50, 60, 70, 80]
])

# K-Means Modell
kmeans = KMeans(n_clusters=6)
clusters = kmeans.fit_predict(data)

# PCA zur Reduzierung der Dimensionalität für die Visualisierung
pca = PCA(n_components=6)
pca_result = pca.fit_transform(data)

# Visualisierung
plt.figure(figsize=(8, 6))
scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], c=clusters, cmap='viridis', marker='o', edgecolor='k', s=100)
plt.title('Visualisierung der Cluster')
plt.xlabel('PCA Komponente 1')
plt.ylabel('PCA Komponente 2')
plt.colorbar(scatter, label='Cluster')
plt.grid(True)
plt.show()