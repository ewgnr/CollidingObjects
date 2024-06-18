# Importieren der notwendigen Bibliotheken
import sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

# Beispiel-Daten in einem DataFrame
df = pd.DataFrame({
    "NUMBER_OF_COLLISIONS": [10, 20, 10, 30, 60, 70],
    "NUMBER_OF_BALLS": [1, 2, 1, 2, 10, 20],
    "NUMBER_OF_LINES": [0, 3, 0, 4, 5, 7],
    "NUMBER_OF_TELEPORTS": [0, 0, 1, 2, 8, 7],
    "NUMBER_OF_FAILS": [0, 1, 0, 1, 9, 4],
    "PLAY_DURATION": [360, 500, 300, 450, 900, 200]
})

# Wir wählen zwei relevante Features für das 2D-Clustering
X = df[["NUMBER_OF_COLLISIONS", "NUMBER_OF_BALLS"]].values

# Daten normalisieren
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# k-Means Modell erstellen und anpassen
kmeans = KMeans(n_clusters=2, random_state=42, n_init="auto")
kmeans.fit(X_scaled)

# Cluster-Zentren und Zuordnungen ausgeben
cluster_centers = kmeans.cluster_centers_
labels = kmeans.labels_

print("Cluster Centers:\n", cluster_centers)
print("Labels:", labels)

# Visualisierung der Cluster
plt.figure(figsize=(10, 8))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='viridis', marker='o', label='Data points')
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], c='red', marker='x', s=200, label='Cluster centers')
plt.title('k-Means Clustering of 2D Data')
plt.xlabel('NUMBER_OF_COLLISIONS (normalized)')
plt.ylabel('NUMBER_OF_BALLS (normalized)')
plt.legend()
plt.show()
