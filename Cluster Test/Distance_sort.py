import os  # Importieren des Betriebssystemmoduls (in diesem Code jedoch nicht verwendet)
import numpy as np  # Importieren der numpy-Bibliothek für numerische Operationen
from matplotlib import pyplot as plt  # Importieren der pyplot-Schnittstelle von Matplotlib zum Erstellen von Diagrammen (nicht verwendet)
# Definieren von Feature-Namen (wird in diesem Code nicht weiter verwendet)
features = ["f1", "f2", "f3", "f4", "f5"]
# Definieren von numerischen Arrays
list1 = np.array([1, 2, 3, 4, 5])  # Erstes Array
list2 = np.array([7, 9, 45, 23, 12])  # Zweites Array
list3 = np.array([21, 32, 13, 14, 17])  # Drittes Array
# Gruppieren der Arrays in einer Liste
lists = [list1, list2, list3]
# Initialisieren einer leeren Liste zum Speichern der euklidischen Normen
list_nn_distances = []

# Berechnen der euklidischen Normen für jedes Array in 'lists'
for list in lists:
    # Berechnen der euklidischen Norm (L2-Norm) des aktuellen Arrays
    nn_distances = np.linalg.norm(list)
    
    # Hinzufügen der berechneten Norm zur Liste 'list_nn_distances'
    list_nn_distances.append(nn_distances)
    
    # Ausgabe der berechneten Norm
    print(nn_distances)

# Konvertieren der Liste der Normen in ein numpy-Array
np_list_nn_distances = np.array(list_nn_distances)
# Ausgabe des numpy-Arrays der Normen
print(np_list_nn_distances)
# Sortieren der Indizes der Normen im Array in aufsteigender Reihenfolge
nn_indices = np_list_nn_distances.argsort()
# Ausgabe der sortierten Indizes
print(nn_indices)