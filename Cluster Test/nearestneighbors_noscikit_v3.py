"""
Imports
"""

import os
import numpy as np
import torch
from matplotlib import pyplot as plt
import wave
import time


features = ["f1", "f2", "f3", "f4", "f5"]
list = {[1, 2, 3, 4, 5], [7, 9, 45, 23, 12], [21, 32, 13, 14, 17]}

nn_distances = np.linalg.norm(audio_features_proc - nn_current_feature, axis=1)




"""
Normalise Audio Features
"""

for feature_name in list(features):
    
    #print(audio_feature_name)
    
    feature = features[feature_name]
    
    audio_feature_mean = np.mean(audio_feature)
    audio_feature_std = np.std(audio_feature)
    
    audio_feature_norm = (audio_feature - audio_feature_mean) / audio_feature_std
    
    #print("audio_feature_norm s ", audio_feature_norm.shape)

    audio_features[audio_feature_name + " norm"] = audio_feature_norm
    
"""
Find Nearest Neighbors
"""

# gather all waveforms and audio features
audio_features_proc = []
for audio_feature_name in audio_feature_names:
    audio_norm_feature_name = audio_feature_name + " norm"
    audio_feature = audio_features[audio_norm_feature_name]
    #print("name ", audio_norm_feature_name, " shape ", audio_feature.shape)
    audio_features_proc.append(audio_feature)
    
audio_features_proc = np.concatenate(audio_features_proc, axis=1)
audio_waveforms_proc = np.copy(audio_waveforms)

nn_element_count = audio_features_proc.shape[0]


while nn_element_count > 0:
    
    print("remaining neighbors ", nn_element_count)
    
    # search nearest element
    nn_distances = np.linalg.norm(audio_features_proc - nn_current_feature, axis=1)
    k = 2
    nn_indices = nn_distances.argsort()[:k]

    # replace current element with nearest element
    nn_previous_index = nn_current_index
    nn_current_index = nn_indices[1]
    nn_current_waveform = audio_waveforms_proc[nn_current_index]
    nn_current_feature = audio_features_proc[nn_current_index]
    nn_current_feature = np.expand_dims(nn_current_feature, 0)
    
    nn_element_count -= 1