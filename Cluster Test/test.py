from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
import numpy as np



X = np.array([[1, 2], [1, 4], [1, 0],[10, 2], [10, 4], [10, 0],[39, 17], [40,50], [70,90]])
kmeans = KMeans(n_clusters=4, random_state=0, n_init="auto").fit(X)



# Cluster-Zentren und Zuordnungen ausgeben
cluster_centers = kmeans.cluster_centers_
labels = kmeans.labels_


plt.clf()


plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1])

plt.show()
