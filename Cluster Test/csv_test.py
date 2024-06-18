import pandas as pd

# CSV-Datei lesen
df = pd.read_csv(r'C:\EigeneDaten\Semester_24-24\Software Projekt 2\code\Cluster Test\data.csv')

# Konvertiere den DataFrame in eine Liste von Listen
data = df.values.tolist()

# Formatierte Ausgabe ohne Kommas
formatted_output = "[[" + "][".join([" ".join(map(str, row)) for row in data]) + "]]"

# Erste 5 Zeilen der Datei anzeigen
print("Erste 5 Zeilen:")
print(formatted_output)

# Grundlegende Informationen über die Datei anzeigen
print("\nGrundlegende Informationen:")
print(df.info())

# Statistische Beschreibung der Daten
print("\nStatistische Beschreibung:")
print(df.describe())
