
import os
import numpy as np

from matplotlib import pyplot as plt




features = ["f1", "f2", "f3", "f4", "f5"]
list1 =np.array([1, 2, 3, 4, 5])
list2 =np.array([7, 9, 45, 23, 12])
list3 = np.array([21, 32, 13, 14, 17])

lists = [list1, list2, list3]

list_nn_distances = []

for list in lists:
    
    nn_distances = np.linalg.norm(list)
    
    list_nn_distances.append(nn_distances)
    print(nn_distances)
    
    
np_list_nn_distances = np.array(list_nn_distances)

print(np_list_nn_distances)

nn_indices = np_list_nn_distances.argsort()

print(nn_indices)
