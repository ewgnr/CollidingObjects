import numpy as np 
import random
import time 
import pandas as pd
import os


def get_random_np_array():
    return np.array([np.random.randint(10, 70),     # COLLISIONS
                     np.random.randint(50,100 ),    # BALLS
                     np.random.randint(10, 40),     # LINES
                     np.random.randint(0, 12),      # TELEPORTS
                     random.randint(0, 10),         # FAILS
                     np.random.randint(100, 1000)]) # DURATION

data = []


anzahl_random_np_arrays = 1

for i in range(anzahl_random_np_arrays):
    data.append(get_random_np_array())

data = np.array(data)

# Pfad anpassen 

csv_file_path = r'C:\EigeneDaten\Semester_24-24\Software Projekt 2\code\Cluster Test\data.csv'




file_exists = os.path.isfile(csv_file_path)

# Numpy-Array an die CSV-Datei anhängen
with open(csv_file_path, 'a') as f:
    if not file_exists:
        # Header hinzufügen, wenn die Datei neu erstellt wird
        header = 'COLLISIONS,BALLS,LINES,TELEPORTS,FAILS,DURATION\n'
        f.write(header)
    # Daten hinzufügen
    np.savetxt(f, data, delimiter=',', fmt='%d')

print("Daten wurden an 'output.csv' angehängt.")

# Pfad anpassen 

df = pd.read_csv(r'C:\EigeneDaten\Semester_24-24\Software Projekt 2\code\Cluster Test\data.csv')

#CSV to numpy array
data_csv = df.to_numpy()



merged_data = np.concatenate((data, data_csv), axis=0)
print(merged_data)

# Shuffle the data
np.random.shuffle(merged_data)

# Set random seed for reproducibility 
random.seed(0)

# Initialise centroids, number of k clusters
centroids = merged_data[random.sample(range(merged_data.shape[0]), 6)]

# Create a list to store which centroid is assigned to each dataset
assigned_centroids = np.zeros(len(merged_data), dtype = np.int32)


def compute_l2_distance(x, centroid):
    # Compute the difference, following by raising to power 2 and summing
    dist = ((x - centroid) ** 2).sum(axis = x.ndim - 1)
    
    return dist

def get_closest_centroid(x, centroids):
    
    # Loop over each centroid and compute the distance from data point.
    dist = compute_l2_distance(x, centroids)

    # Get the index of the centroid with the smallest distance to the data point 
    closest_centroid_index =  np.argmin(dist, axis = 1)
    
    return closest_centroid_index

def compute_sse(data, centroids, assigned_centroids):
    # Initialise SSE 
    sse = 0

    # Compute SSE
    sse = compute_l2_distance(data, centroids[assigned_centroids]).sum() / len(merged_data)
    
    return sse


# Number of dimensions in centroid
num_centroid_dims = merged_data.shape[1]

# List to store SSE for each iteration 
sse_list = []

# Start time
tic = time.time()

# Main Loop
for n in range(50):
    # Get closest centroids to each data point
    assigned_centroids = get_closest_centroid(merged_data[:, None, :], centroids[None,:, :])    
    
    # Compute new centroids
    for c in range(centroids.shape[1]):
        # Get data points belonging to each cluster 
        cluster_members = merged_data[assigned_centroids == c]
        
        # Compute the mean of the clusters
        cluster_members = cluster_members.mean(axis = 0)
        
        # Update the centroids
        centroids[c] = cluster_members
    
    # Compute SSE
    sse = compute_sse(merged_data.squeeze(), centroids.squeeze(), assigned_centroids)
    sse_list.append(sse)

# End time
toc = time.time()

print(round(toc - tic, 4)/50)
   
     
index = np.argsort(assigned_centroids)
sorted_data = np.array(merged_data)[index]
sorted_centroids = np.sort(assigned_centroids)

for i in range(len(sorted_data)):
    print('data {0}, cluster {1}'.format(sorted_data[i], sorted_centroids[i]))

    