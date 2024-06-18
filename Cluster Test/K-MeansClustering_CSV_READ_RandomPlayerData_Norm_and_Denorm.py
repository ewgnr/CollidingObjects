import numpy as np 
import random
import time 
import pandas as pd
import os


def get_random_np_array():
    return np.array([np.random.randint(100, 1000),  # COLLISIONS
                     np.random.randint(100, 1000),  # BALLS
                     np.random.randint(100, 1000),  # LINES
                     np.random.randint(100, 1000),  # TELEPORTS
                     np.random.randint(100, 1000),  # FAILS
                     np.random.randint(100, 1000),  # DURATION
                     np.random.randint(100,1000)])  #Harmonicity
    

data = []


anzahl_random_np_arrays = 20

for i in range(anzahl_random_np_arrays):
    data.append(get_random_np_array())

data = np.array(data)

print (data)
"""
Normalisierung der Daten
"""
Collisions = data[:, 0]
BALLS = data[:, 1]
LINES= data[:, 2]
TELEPORTS = data[:, 3]
FAILS = data[:, 4]
DURATION = data[:, 5]
HARMONICITY = data[:, 6]

def calc_norm(data):
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std

norm_collisions = calc_norm(Collisions)
norm_balls = calc_norm(BALLS)
norm_lines = calc_norm(LINES)
norm_teleports = calc_norm(TELEPORTS)
norm_fails= calc_norm(FAILS)
norm_duration= calc_norm(DURATION)
norm_harmonicity = calc_norm(HARMONICITY)

norm_data = np.array([norm_collisions, norm_balls, norm_lines, norm_teleports, norm_fails, norm_duration, norm_harmonicity]).T
print("normData")

print(norm_data)



csv_file_path = r'C:\EigeneDaten\Semester_24-24\Software Projekt 2\code\Cluster Test\preset_number_1.csv'
file_exists = os.path.isfile(csv_file_path)

# Numpy-Array an die CSV-Datei anhängen
with open(csv_file_path, 'a') as f:
    if not file_exists:
        # Header hinzufügen, wenn die Datei neu erstellt wird
        header = 'COLLISIONS,BALLS,LINES,TELEPORTS,FAILS,DURATION,HARMONICITY\n'
        f.write(header)
    # Daten hinzufügen
    np.savetxt(f, data, delimiter=',', fmt='%d')

print("Daten wurden an csv angehängt.")

# Pfad anpassen 

try:
    df = pd.read_csv(r'C:\EigeneDaten\Semester_24-24\Software Projekt 2\code\Cluster Test\preset_number_1.csv')
except pd.errors.ParserError as e:
    print("Error parsing CSV file:", e)
    with open(r'C:\EigeneDaten\Semester_24-24\Software Projekt 2\code\Cluster Test\preset_number_1.csv', 'r') as file:
        for i, line in enumerate(file):
            print(f"Line {i+1}: {line.strip()}")
#CSV to numpy array
data_csv = df.to_numpy()



merged_data = np.concatenate((data, data_csv), axis=0)
print(merged_data)

# Shuffle the data
np.random.shuffle(norm_data)

# Set random seed for reproducibility 
random.seed(0)

# Initialise centroids, number of k clusters
centroids = norm_data[random.sample(range(norm_data.shape[0]), 7)]

# Create a list to store which centroid is assigned to each dataset
assigned_centroids = np.zeros(len(norm_data), dtype = np.int32)


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
    sse = compute_l2_distance(data, centroids[assigned_centroids]).sum() / len(norm_data)
    
    return sse


# Number of dimensions in centroid
num_centroid_dims = norm_data.shape[1]

# List to store SSE for each iteration 
sse_list = []

# Start time
tic = time.time()

# Main Loop
for n in range(50):
    # Get closest centroids to each data point
    assigned_centroids = get_closest_centroid(norm_data[:, None, :], centroids[None,:, :])    
    
    # Compute new centroids
    for c in range(centroids.shape[1]):
        # Get data points belonging to each cluster 
        cluster_members = norm_data[assigned_centroids == c]
        
        # Compute the mean of the clusters
        cluster_members = cluster_members.mean(axis = 0)
        
        # Update the centroids
        centroids[c] = cluster_members
    
    # Compute SSE
    sse = compute_sse(norm_data.squeeze(), centroids.squeeze(), assigned_centroids)
    sse_list.append(sse)

# End time
toc = time.time()

print(round(toc - tic, 4)/50)

"""
Denorminalisierung der Daten
"""

Collisions_ = norm_data[:, 0]
BALLS_ = norm_data[:, 1]
LINES_ = norm_data[:, 2]
TELEPORTS_ = norm_data[:, 3]
FAILS_ = norm_data[:, 4]
DURATION_ = norm_data[:, 5]
HARMONICITY = norm_data[:, 6]



# to make data human readable, return them to the original denormalised form
def re_calc_norm(data, mean, std):
    x = data * std + mean
    return x

# Use the original mean and std for denormalization
re_calc_collisions = re_calc_norm(Collisions_, np.mean(Collisions), np.std(Collisions))
re_calc_balls = re_calc_norm(BALLS_, np.mean(BALLS), np.std(BALLS))
re_calc_lines = re_calc_norm(LINES_, np.mean(LINES), np.std(LINES))
re_calc_teleports = re_calc_norm(TELEPORTS_, np.mean(TELEPORTS), np.std(TELEPORTS))
re_calc_fails = re_calc_norm(FAILS_, np.mean(FAILS), np.std(FAILS))
re_calc_duration = re_calc_norm(DURATION_, np.mean(DURATION), np.std(DURATION))
re_calc_harmonicity = re_calc_norm(HARMONICITY, np.mean(HARMONICITY), np.std(HARMONICITY))

denorminalisated_data = np.array([re_calc_collisions, re_calc_balls, re_calc_lines, re_calc_teleports, re_calc_fails, re_calc_duration, re_calc_harmonicity]).T
print("denorminalisated data")
print(denorminalisated_data)




     
index = np.argsort(assigned_centroids)
sorted_data = np.array(denorminalisated_data)[index]
sorted_centroids = np.sort(assigned_centroids)


for i in range(len(sorted_data)):
    print('data {0}, cluster {1}'.format(sorted_data[i], sorted_centroids[i]))

