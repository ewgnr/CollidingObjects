import numpy as np 
import random
import time 
import pandas as pd


def get_random_np_array_0_100():
    random_int_array = np.random.randint(0, 100, 6)
    random_int_np_array = random_int_array.reshape(1, -1)
    return random_int_np_array


def get_random_np_array():
    colission = np.random.randint(0, 20)
    BALLS = np.random.randint(50,100 )
    Lines = np.random.randint(10, 40)
    Teleports = np.random.randint(0, 12)
    Fails = np.random.randint(0, 10)
    duration = np.random.randint(100, 1000)



    random_int_array = np.array([colission, BALLS, Lines, Teleports, Fails, duration])


    random_int_np_array = random_int_array.reshape(1, -1)
    return random_int_np_array



df = pd.DataFrame({
    "NUMBER_OF_COLLISIONS": [10,   20,  10,  30, 60, 70],
    "NUMBER_OF_BALLS":      [1,    2,   1,   2, 10,20],
    "NUMBER_OF_LINES":      [0,    3,   0,   4, 5,7],
    "NUMBER_OF_TELEPORTS":  [0,    0,   1,   2,8, 7],
    "NUMBER_OF_FAILS":      [0,    1,   0,   1, 9,4],
    "PLAY_DURATION":        [360,  500, 300, 450, 900,200]
})

data = np.array([[10, 1,  0, 0, 0, 360], [20, 2,  3, 0, 1, 500], [10, 1,  0, 1, 0, 300], 
                 [29, 2,  3, 5, 1, 200], [60, 10, 5, 8, 9, 900], [35, 17, 9, 2, 4, 800],
                 [30, 2,  4, 2, 1, 450], [60, 10, 5, 8, 9, 100], [70, 20, 7, 7, 4, 200], [31, 3, 5, 3, 0, 460]])


for i in range(df.shape[0]):
    row_array = df.iloc[i, :].to_numpy().reshape(1, -1)
    data = np.append(data, row_array, axis=0)

anzahl_random_np_arrays = 10

for i in range(anzahl_random_np_arrays):
    random_int_np_array = get_random_np_array()
    data = np.append(data, random_int_np_array, axis=0)

print(data)

# Shuffle the data
np.random.shuffle(data)

# Set random seed for reproducibility 
random.seed(0)

# Initialise centroids, number of k clusters
centroids = data[random.sample(range(data.shape[0]), 6)]

# Create a list to store which centroid is assigned to each dataset
assigned_centroids = np.zeros(len(data), dtype = np.int32)


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
    sse = compute_l2_distance(data, centroids[assigned_centroids]).sum() / len(data)
    
    return sse


# Number of dimensions in centroid
num_centroid_dims = data.shape[1]

# List to store SSE for each iteration 
sse_list = []

# Start time
tic = time.time()

# Main Loop
for n in range(50):
    # Get closest centroids to each data point
    assigned_centroids = get_closest_centroid(data[:, None, :], centroids[None,:, :])    
    
    # Compute new centroids
    for c in range(centroids.shape[1]):
        # Get data points belonging to each cluster 
        cluster_members = data[assigned_centroids == c]
        
        # Compute the mean of the clusters
        cluster_members = cluster_members.mean(axis = 0)
        
        # Update the centroids
        centroids[c] = cluster_members
    
    # Compute SSE
    sse = compute_sse(data.squeeze(), centroids.squeeze(), assigned_centroids)
    sse_list.append(sse)

# End time
toc = time.time()

print(round(toc - tic, 4)/50)
   
     
sorted_data = []
sorted_centroids = np.sort(assigned_centroids)     
for i in range(len(assigned_centroids)):
    sorted_data.append(data[sorted_centroids[i]])
    print('player data {0}, cluster {1}.'.format(data[sorted_centroids[i]], sorted_centroids[i]))

    