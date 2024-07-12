import numpy as np 
import random
import pandas as pd

import argparse
import time

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# Send OSC
send_parser = argparse.ArgumentParser()
send_parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
send_parser.add_argument("--port", type=int, default=7001, help="The port the OSC server is listening on")
send_args = send_parser.parse_args()

client = udp_client.SimpleUDPClient(send_args.ip, send_args.port)

# Message Handler
def receive_values_handler(unused_addr, args, volume):    

    valueFromOF = volume

    if valueFromOF == True:
        
        # Set random seed for reproducibility 
        random.seed(0)
        
        # load csv file
        raw_data = pd.read_csv('player_values_1.csv')
        string_data = raw_data.dropna()
            
        data = np.array(string_data, dtype = np.int32)
        
        # time.sleep(1)
        
        # Normalize Data
        def calc_norm(data):
            mean = np.mean(data)
            std = np.std(data)
            return (data - mean) / std
        
        norm_collisions = calc_norm(data[:, 0])
        norm_balls = calc_norm(data[:, 1])
        norm_lines = calc_norm(data[:, 2])
        norm_teleports = calc_norm(data[:, 3])
        norm_fails= calc_norm(data[:, 4])
        norm_harmonicity = calc_norm(data[:, 5])
        norm_duration = calc_norm(data[:, 6])
        
        norm_data = np.array([norm_collisions, norm_balls, norm_lines, norm_teleports, norm_fails, norm_harmonicity, norm_duration]).T
        
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
        
        # List to store SSE for each iteration 
        sse_list = []
        
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
        
        
        # Denormalize, make data human readable
        def denorm(data, mean, std):
            x = data * std + mean
            return x
        
        # Use the original mean and std for denormalization
        collisions = denorm(norm_data[:, 0], np.mean(data[:, 0]), np.std(data[:, 0]))
        balls = denorm(norm_data[:, 1], np.mean(data[:, 1]), np.std(data[:, 1]))
        lines = denorm(norm_data[:, 2], np.mean(data[:, 2]), np.std(data[:, 2]))
        teleports = denorm(norm_data[:, 3], np.mean(data[:, 3]), np.std(data[:, 3]))
        fails = denorm(norm_data[:, 4], np.mean(data[:, 4]), np.std(data[:, 4]))
        harmonicity = denorm(norm_data[:, 5], np.mean(data[:, 5]), np.std(data[:, 5]))
        duration = denorm(norm_data[:, 6], np.mean(data[:, 6]), np.std(data[:, 6]))
        
        denorm_data = np.array([collisions, balls, lines, teleports, fails, duration, harmonicity]).T
        
        # Print calculated clusters
        index = np.argsort(assigned_centroids)
        sorted_data = np.array(denorm_data)[index]
        sorted_centroids = np.sort(assigned_centroids)
        
        for i in range(len(sorted_centroids)):
            print('data {0}, cluster {1}'.format(sorted_data[i], sorted_centroids[i]))
        
        # Calculating max and min values from each cluster
        max_values_for_each_cluster = np.empty((0,7), dtype=int)
        min_values_for_each_cluster = np.empty((0,7), dtype=int)
        sorted_max_values = np.empty((0,7), dtype=int)
        sorted_min_values = np.empty((0,7), dtype=int)
        
        for i in range(len(sorted_centroids)):
            max_and_min = np.empty((0,7), dtype=int)
            for j in range(len(sorted_data)):
                if sorted_centroids[j] == i:
                    print(sorted_data[j], i)
                    max_and_min = np.append(max_and_min, np.array([sorted_data[j]]), axis=0)
        
            if np.size(max_and_min) != 0:
                max_values_for_each_cluster = np.array([max_and_min.max(axis=0)])
                min_values_for_each_cluster = np.array([max_and_min.min(axis=0)])            
        
                sorted_max_values = np.append(sorted_max_values, np.array(max_values_for_each_cluster), axis=0)
                sorted_min_values = np.append(sorted_min_values, np.array(min_values_for_each_cluster), axis=0)
            
        # Find cluster, depending on latest player data
        actual_player_data = np.array([data[-1]], dtype=int) 
        for i in range(len(sorted_centroids)):
            if np.all(actual_player_data[0]) == np.all(sorted_data[i]):
                player_cluster_index = sorted_centroids[i]
          
        norm_max_collisions = calc_norm(sorted_max_values[:, 0])
        norm_max_balls = calc_norm(sorted_max_values[:, 1])
        norm_max_lines = calc_norm(sorted_max_values[:, 2])
        norm_max_teleports = calc_norm(sorted_max_values[:, 3])
        norm_max_fails= calc_norm(sorted_max_values[:, 4])
        norm_max_harmonicity = calc_norm(sorted_max_values[:, 5])
        norm_max_duration = calc_norm(sorted_max_values[:, 6])
        
        norm_sorted_max_values = np.stack((norm_max_collisions, norm_max_balls, norm_max_lines, norm_max_teleports, norm_max_fails, norm_max_harmonicity, norm_max_duration), axis=-1)
        
        cluster_name_indecies = norm_sorted_max_values.argmin(axis=1)
        cluster_names = ['collisions', 'balls', 'lines', 'teleports', 'fails', 'harmonicity', 'duration']
          
        client.send_message("/player_values", 
                            [cluster_names[cluster_name_indecies[player_cluster_index]], 
                            sorted_min_values[player_cluster_index][0],
                            sorted_min_values[player_cluster_index][1],
                            sorted_min_values[player_cluster_index][2],
                            sorted_min_values[player_cluster_index][3],
                            sorted_min_values[player_cluster_index][4],
                            sorted_min_values[player_cluster_index][5],
                            sorted_min_values[player_cluster_index][6],
                            sorted_max_values[player_cluster_index][0],
                            sorted_max_values[player_cluster_index][1],
                            sorted_max_values[player_cluster_index][2],
                            sorted_max_values[player_cluster_index][3],
                            sorted_max_values[player_cluster_index][4],
                            sorted_max_values[player_cluster_index][5],
                            sorted_max_values[player_cluster_index][6],
                            int(actual_player_data[0][0]),
                            int(actual_player_data[0][1]),
                            int(actual_player_data[0][2]),
                            int(actual_player_data[0][3]),
                            int(actual_player_data[0][4]),
                            int(actual_player_data[0][5]),
                            int(actual_player_data[0][6]),
                            np.max(sorted_data)])
        
    valueFromOF = False
    print(valueFromOF)	

# Receive OSC
receive_parser = argparse.ArgumentParser()
receive_parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
receive_parser.add_argument("--port", type=int, default=7000, help="The port to listen on")
receive_args = receive_parser.parse_args()

dispatcher = Dispatcher() 
dispatcher.map("/read_file", receive_values_handler, "read_file")

server = osc_server.ThreadingOSCUDPServer((receive_args.ip, receive_args.port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
