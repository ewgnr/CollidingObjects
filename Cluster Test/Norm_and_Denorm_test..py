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


anzahl_random_np_arrays = 10

for i in range(anzahl_random_np_arrays):
    data.append(get_random_np_array())

data = np.array(data)

print ('data')
print (data)

Collisions = data[:, 0]
BALLS = data[:, 1]
LINES= data[:, 2]
TELEPORTS = data[:, 3]
FAILS = data[:, 4]
DURATION = data[:, 5]


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

norm_data = np.array([norm_collisions, norm_balls, norm_lines, norm_teleports, norm_fails, norm_duration]).T
print("normData")
print(norm_data)


Collisions_ = norm_data[:, 0]
BALLS_ = norm_data[:, 1]
LINES_ = norm_data[:, 2]
TELEPORTS_ = norm_data[:, 3]
FAILS_ = norm_data[:, 4]
DURATION_ = norm_data[:, 5]



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

re_calc_data = np.array([re_calc_collisions, re_calc_balls, re_calc_lines, re_calc_teleports, re_calc_fails, re_calc_duration]).T
print("re_calc_data")
print(re_calc_data)
