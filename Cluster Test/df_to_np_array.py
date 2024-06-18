import numpy as np

# Generieren eines Arrays mit 5 zufälligen ganzzahligen Werten im Bereich von 0 bis 100
random_int_values = np.random.randint(0, 100, 5)

# Anzeigen des erstellten Arrays
print("Random Integer Values:", random_int_values)

# Optional: Umwandeln in ein 2D-Array, falls nötig
random_int_values_2d = random_int_values.reshape(1, -1)

print("Random Integer Values (2D):", random_int_values_2d)