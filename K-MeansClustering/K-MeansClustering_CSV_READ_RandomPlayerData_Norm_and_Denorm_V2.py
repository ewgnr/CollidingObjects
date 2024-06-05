'''
csv_file_path = r'C:/Users/ephra/Documents/Lehre/BasicsOfML/K-MeansClustering/preset_number_1.csv'
file_exists = os.path.isfile(csv_file_path)

# Numpy-Array an die CSV-Datei anhängen
with open(csv_file_path, 'a') as f:
    if not file_exists:
        # Header hinzufügen, wenn die Datei neu erstellt wird
        header = 'COLLISIONS,BALLS,LINES,TELEPORTS,FAILS,DURATION,HARMONICITY\n'
        f.write(header)
    # Daten hinzufügen
    np.savetxt(f, data, delimiter=',', fmt='%d')

print("Daten wurden an 'output.csv' angehängt.")
'''

import numpy as np 
import random
import time 
import pandas as pd

# Set random seed for reproducibility 
random.seed(0)

# generate random data
def get_random_np_array_group_1():
    return np.array([np.random.randint(100, 1000),  # COLLISIONS
                     np.random.randint(10, 50),     # BALLS
                     np.random.randint(4, 16),      # LINES
                     np.random.randint(0, 3),       # TELEPORTS
                     np.random.randint(1, 10),      # FAILS
                     np.random.randint(700, 1000),  # DURATION
                     np.random.randint(30, 70)])    # HARMONICITY

def get_random_np_array_group_2():
    return np.array([np.random.randint(0, 10),      # COLLISIONS
                     np.random.randint(100, 101),   # BALLS
                     np.random.randint(0, 2),       # LINES
                     np.random.randint(0, 1),       # TELEPORTS
                     np.random.randint(100, 101),   # FAILS
                     np.random.randint(10, 200),    # DURATION
                     np.random.randint(0, 2)])      # HARMONICITY

def get_random_np_array_group_3():
    return np.array([np.random.randint(10, 50),     # COLLISIONS
                     np.random.randint(10, 20),     # BALLS
                     np.random.randint(700, 1000),  # LINES
                     np.random.randint(0, 4),       # TELEPORTS
                     np.random.randint(10, 20),     # FAILS
                     np.random.randint(800, 2000),  # DURATION
                     np.random.randint(10, 20)])    # HARMONICITY

def get_random_np_array_group_4():
    return np.array([np.random.randint(400, 800),   # COLLISIONS
                     np.random.randint(50, 100),    # BALLS
                     np.random.randint(12, 20),     # LINES
                     np.random.randint(400, 800),   # TELEPORTS
                     np.random.randint(20, 30),     # FAILS
                     np.random.randint(200, 700),   # DURATION
                     np.random.randint(90, 100)])   # HARMONICITY

def get_random_np_array_group_5():
    return np.array([np.random.randint(0, 10),      # COLLISIONS
                     np.random.randint(0, 10),      # BALLS
                     np.random.randint(0, 10),      # LINES
                     np.random.randint(0, 2),       # TELEPORTS
                     np.random.randint(0, 100),     # FAILS
                     np.random.randint(2500, 3000), # DURATION
                     np.random.randint(0, 3)])      # HARMONICITY

def get_random_np_array_group_6():
    return np.array([np.random.randint(30, 50),     # COLLISIONS
                     np.random.randint(10, 25),     # BALLS
                     np.random.randint(4, 12),      # LINES
                     np.random.randint(30, 40),     # TELEPORTS
                     np.random.randint(2, 3),       # FAILS
                     np.random.randint(800, 1000),  # DURATION
                     np.random.randint(90, 100)])   # HARMONICITY


data = []
anzahl_random_np_arrays = 20

for i in range(anzahl_random_np_arrays):
    data.append(get_random_np_array_group_1())
    data.append(get_random_np_array_group_2())
    data.append(get_random_np_array_group_3())
    data.append(get_random_np_array_group_4())
    data.append(get_random_np_array_group_5())
    data.append(get_random_np_array_group_6())

# load csv file
# df = pd.read_csv(r'C:/Users/ephra/Documents/Lehre/BasicsOfML/K-MeansClustering/preset_number_1.csv')

data = np.array(data)
# data = np.concatenate((data, df.to_numpy()), axis=0)


"""
Normalisierung der Daten
"""
COLLISIONS = data[:, 0]
BALLS = data[:, 1]
LINES = data[:, 2]
TELEPORTS = data[:, 3]
FAILS = data[:, 4]
DURATION = data[:, 5]
HARMONICITY = data[:, 6]


def calc_norm(data):
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std

norm_collisions = calc_norm(COLLISIONS)
norm_balls = calc_norm(BALLS)
norm_lines = calc_norm(LINES)
norm_teleports = calc_norm(TELEPORTS)
norm_fails= calc_norm(FAILS)
norm_duration = calc_norm(DURATION)
norm_harmonicity = calc_norm(HARMONICITY)

norm_data = np.array([norm_collisions, norm_balls, norm_lines, norm_teleports, norm_fails, norm_duration, norm_harmonicity]).T

# Shuffle the data
np.random.shuffle(norm_data)

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
COLLISIONS_ = norm_data[:, 0]
BALLS_ = norm_data[:, 1]
LINES_ = norm_data[:, 2]
TELEPORTS_ = norm_data[:, 3]
FAILS_ = norm_data[:, 4]
DURATION_ = norm_data[:, 5]
HARMONICITY_ = norm_data[:, 6]


# to make data human readable, return them to the original denormalised form
def re_calc_norm(data, mean, std):
    x = data * std + mean
    return x

# Use the original mean and std for denormalization
re_calc_collisions = re_calc_norm(COLLISIONS_, np.mean(COLLISIONS), np.std(COLLISIONS))
re_calc_balls = re_calc_norm(BALLS_, np.mean(BALLS), np.std(BALLS))
re_calc_lines = re_calc_norm(LINES_, np.mean(LINES), np.std(LINES))
re_calc_teleports = re_calc_norm(TELEPORTS_, np.mean(TELEPORTS), np.std(TELEPORTS))
re_calc_fails = re_calc_norm(FAILS_, np.mean(FAILS), np.std(FAILS))
re_calc_duration = re_calc_norm(DURATION_, np.mean(DURATION), np.std(DURATION))
re_calc_harmonicity = re_calc_norm(HARMONICITY_, np.mean(HARMONICITY), np.std(HARMONICITY))

denorminalisated_data = np.array([re_calc_collisions, re_calc_balls, re_calc_lines, re_calc_teleports, re_calc_fails, re_calc_duration, re_calc_harmonicity]).T

# print calculated clusters
index = np.argsort(assigned_centroids)
sorted_data = np.array(denorminalisated_data)[index]
sorted_centroids = np.sort(assigned_centroids)

for i in range(len(sorted_data)):
    print('data {0}, cluster {1}'.format(sorted_data[i], sorted_centroids[i]))

