# Importieren der notwendigen Bibliotheken
from mpl_toolkits import mplot3d  # Importieren des 3D-Plot-Moduls von Matplotlib
import numpy as np  # Importieren der numpy-Bibliothek für numerische Operationen
import matplotlib.pyplot as plt  # Importieren der pyplot-Schnittstelle von Matplotlib zum Erstellen von Diagrammen

"""
 1 for fails 
 10, for teleports
 20 for lines 
 30 for balls 
 40 for collisions
"""
# Erstellen des Datensatzes
# Die folgenden Listen enthalten die Datenpunkte für die x-, y- und z-Koordinaten
z = [1, 10, 20, 30, 40, 1, 10, 20, 30, 40]  # z-Koordinaten
x = [7, 8, 6, 8, 30, 12, 5, 13, 40, 60]  # x-Koordinaten
y = [1, 10, 20, 30, 40, 1, 10, 20, 30, 40]  # y-Koordinaten
color_array = [5, 5, 5, 5, 5, 6, 6, 6, 6, 6]  # Farbcodes für die Punkte im Diagramm

# Erstellen der Figur
fig = plt.figure(figsize = (15, 99))  # Erstellen einer Figur mit spezifischer Größe
ax = plt.axes(projection ="3d")  # Hinzufügen eines 3D-Achsensystems zur Figur

# Erstellen des Streudiagramms
# Die Methode scatter3D() erstellt ein 3D-Streudiagramm mit den x-, y- 
# und z-Koordinaten und färbt die Punkte entsprechend der color_array-Liste ein
ax.scatter3D(x, y, z, c=color_array, cmap='viridis')

# Hinzufügen eines Titels zum Diagramm
plt.title("simple 3D scatter plot")

# Anzeigen des Diagramms
plt.show()  # Zeigt das erstellte 3D-Streudiagramm an
