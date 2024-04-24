import sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np


# Angenommen, deine Daten sind in einem DataFrame df
df = pd.DataFrame({
    "NUMBER_OF_COLLISIONS": [10, 20, 10, 30, 60, 70],
    "NUMBER_OF_BALLS": [1, 2, 1, 2, 10,20],
    "NUMBER_OF_LINES": [0, 3, 0, 4, 5,7],
    "NUMBER_OF_TELEPORTS": [0, 0, 1, 2,8, 7],
    "NUMBER_OF_FAILS": [0, 1, 0, 1, 9,4],
    "PLAY_DURATION": [360, 500, 300, 450, 900,200]
})

X = np.array([
               [0, 1], 
               [0, 5],
               [0, 3], 
              [1, 2], 
              [10, 20]])


# Daten normalisieren
#scaler = StandardScaler()
#df_scaled = scaler.fit_transform(df)

# k-Means Modell erstellen und anpassen
kmeans = KMeans(n_clusters=2, random_state=42, n_init="auto").fit(X)
#kmeans.fit(df)

# Cluster-Zentren und Zuordnungen ausgeben
cluster_centers = kmeans.cluster_centers_
labels = kmeans.labels_

print("Cluster Centers:\n", cluster_centers)
print("Labels:", labels)

print(cluster_centers[1:] )

#:1  [[ 0.30151134  1.          0.70014004 -0.90453403  1.          1.25675744]]
#1: [[-0.90453403 -1.         -0.98019606  0.30151134 -1.         -1.32120654]
# [-0.90453403 -1.         -0.98019606 -0.90453403 -1.         -0.54781734]
# [ 1.50755672  1.          1.26025208  1.50755672  1.          0.61226644]]


#axs[0, 0].scatter(X[:, 0], X[:, 1], c=y)


plt.clf()


plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1],  c=labels)

plt.show()