"""
Imports
"""

import os
import numpy as np
import librosa
import torch
import torchaudio
import audio_analysis
from matplotlib import pyplot as plt
import wave
import time

"""
Audio Settings
"""

audio_file_path = "D:/Data/audio/DanielBisig/ostrawa_recordings_selection"
audio_file_extensions = ["wav", "aiff", "aif"] 
audio_sample_rate = 48000
audio_sample_count = audio_sample_rate // 1
audio_sample_offset = audio_sample_count // 2

audio_feature_names = ["root mean square", "mfcc"]

"""
Load Audio
"""

audio_waveforms_full = []

for root, _, fnames in sorted(os.walk(audio_file_path, followlinks=True)):
    for fname in sorted(fnames):
        
        path = root + "/" + fname
        
        print("path ", path)
        
        audio_waveform, _ = librosa.load(path, sr=audio_sample_rate)

        print("waveform s ", audio_waveform.shape)
        
        audio_waveforms_full.append(audio_waveform)

"""
Create Audio Excerpts
"""

audio_waveform_excerpts = []

for waveform_full in audio_waveforms_full:
    waveform_sample_count = waveform_full.shape[0]
    for sI in range(0, waveform_sample_count - audio_sample_count, audio_sample_offset):
        waveform_except = waveform_full[sI:sI + audio_sample_count]
        audio_waveform_excerpts.append(waveform_except)
        
audio_waveforms = np.stack(audio_waveform_excerpts, axis=0)
        
"""
Calculate Audio Features
"""

audio_features = {}

audio_features["waveform"] = audio_waveforms
if "root mean square" in audio_feature_names:
    audio_features["root mean square"] = audio_analysis.rms(audio_waveforms)
if "chroma stft" in audio_feature_names:
    audio_features["chroma stft"] = audio_analysis.chroma_stft(audio_waveforms, audio_sample_rate)
if "chroma cqt" in audio_feature_names:
    audio_features["chroma cqt"] = audio_analysis.chroma_cqt(audio_waveforms, audio_sample_rate)
if "chroma cens" in audio_feature_names:
    audio_features["chroma cens"] = audio_analysis.chroma_cens(audio_waveforms, audio_sample_rate)
if "chroma vqt" in audio_feature_names:
    audio_features["chroma vqt"] = audio_analysis.chroma_vqt(audio_waveforms, audio_sample_rate)
if "mel spectrogram" in audio_feature_names:
    audio_features["mel spectrogram"] = audio_analysis.mel_spectrogram(audio_waveforms, audio_sample_rate)
if "mfcc" in audio_feature_names:
    audio_features["mfcc"] = audio_analysis.mfcc(audio_waveforms, audio_sample_rate)
if "spectral centroid" in audio_feature_names:
    audio_features["spectral centroid"] = audio_analysis.spectral_centroid(audio_waveforms, audio_sample_rate)
if "spectral bandwidth" in audio_feature_names:
    audio_features["spectral bandwidth"] = audio_analysis.spectral_bandwidth(audio_waveforms, audio_sample_rate)
if "spectral contrast" in audio_feature_names:
    audio_features["spectral contrast"] = audio_analysis.spectral_contrast(audio_waveforms, audio_sample_rate)
if "spectral flatness" in audio_feature_names:
    audio_features["spectral flatness"] = audio_analysis.spectral_flatness(audio_waveforms)
if "spectral rolloff" in audio_feature_names:
    audio_features["spectral rolloff"] = audio_analysis.spectral_rolloff(audio_waveforms, audio_sample_rate)
if "tempo" in audio_feature_names:
    audio_features["tempo"] = audio_analysis.tempo(audio_waveforms, audio_sample_rate)
if "tempogram" in audio_feature_names:
    audio_features["tempogram"] = audio_analysis.tempogram(audio_waveforms, audio_sample_rate)
if "tempogram ratio" in audio_feature_names:
    audio_features["tempogram ratio"] = audio_analysis.tempogram_ratio(audio_waveforms, audio_sample_rate)

"""
Normalise Audio Features
"""

for audio_feature_name in list(audio_features.keys()):
    
    #print(audio_feature_name)
    
    audio_feature = audio_features[audio_feature_name]
    
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

# select first audio feature to begin search with
nn_current_index = 0
nn_current_waveform = audio_waveforms_proc[nn_current_index]
nn_current_feature = audio_features_proc[nn_current_index]
nn_current_feature = np.expand_dims(nn_current_feature, 0)

# prepare empty waveform to copy waveforms corresponding to nearest features into
nn_element_count = audio_features_proc.shape[0]
gen_waveform_sample_count = 2 * audio_sample_count + (nn_element_count - 1) * audio_sample_offset
gen_waveform = np.zeros(gen_waveform_sample_count)

# create amplitude enevelope for blending audio waveforms into gen_waveform
audio_sample_overlap = audio_sample_count - audio_sample_offset
hann_window = torch.hann_window(audio_sample_overlap * 2).numpy()

amplitude_envelope = np.ones([audio_sample_count])
amplitude_envelope[:audio_sample_overlap] *= hann_window[:audio_sample_overlap]
amplitude_envelope[-audio_sample_overlap:] *= hann_window[audio_sample_overlap:]

#plt.plot(amplitude_envelope)

# add first waveform to gen waveform
gen_waveform[:audio_sample_count] += nn_current_waveform * amplitude_envelope

# iterate through all neighbors
sI = audio_sample_count -  audio_sample_overlap # sample index for waveform insertion in gen waveform

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
    
    # blend waveform corresponding to current element into gen waveform
    gen_waveform[sI:sI + audio_sample_count] += nn_current_waveform * amplitude_envelope
    
    # remove previous element
    if nn_previous_index == 0:
        audio_waveforms_proc = np.copy(audio_waveforms_proc[nn_previous_index + 1:])
        audio_features_proc = np.copy(audio_features_proc[nn_previous_index + 1:])
    elif nn_previous_index == audio_waveforms_proc.shape[0] - 1:
        audio_waveforms_proc = np.copy(audio_waveforms_proc[:nn_previous_index])
        audio_features_proc = np.copy(audio_features_proc[:nn_previous_index])
    else:
        audio_waveforms_proc = np.copy(np.concatenate([audio_waveforms_proc[:nn_previous_index], audio_waveforms_proc[nn_previous_index + 1:]], axis=0))
        audio_features_proc = np.copy(np.concatenate([audio_features_proc[:nn_previous_index], audio_features_proc[nn_previous_index + 1:]], axis=0))

    nn_element_count -= 1
    sI += audio_sample_count - audio_sample_overlap


#plt.plot(gen_waveform)

"""
save generated waveform
"""

gen_waveform = torch.tensor(gen_waveform)
gen_waveform = gen_waveform.unsqueeze(0)
torchaudio.save("gen_waveform.wav", gen_waveform, audio_sample_rate)
