#include "ofApp.h"
#include <fstream>
#include <sstream>


//--------------------------------------------------------------
void ofApp::setup(){

}

//--------------------------------------------------------------
void ofApp::update(){

}

//--------------------------------------------------------------
void ofApp::draw(){

}

//--------------------------------------------------------------
void ofApp::keyPressed(int key)
{
    if (key == 'o') readValuesFromFile("1");
    if (key == 's') saveValuesAsFile("1");
}

void ofApp::saveValuesAsFile(const std::string& selectFileNumber)
{
    std::ostringstream Values_for_csv;       // Stream zum Speichern der Werte für CSV
    std::ostringstream Values_Names_for_csv; // Stream zum Speichern der Namen der Werte für CSV
    std::ostringstream allValues;            // Stream zum Speichern aller Werte und Namen für CSV

    // Sammeln der Werte für CSV
    for (int i = 0; i < values.size(); ++i) {
        std::cout << values[i] << "  "; // Ausgabe der Werte zur Kontrolle

        if (i != 6) {
            Values_for_csv << values[i] << ","; // Werte mit Komma trennen
        }
        else {
            Values_for_csv << values[i]; // Letzten Wert ohne Komma hinzufügen
            break;
        }
    }
    Values_for_csv << std::endl; // Zeilenumbruch nach den Werten

    // Sammeln der Namen der Werte für CSV
    for (int i = 0; i < valueNames.size(); ++i) {
        if (i != 6) {
            Values_Names_for_csv << valueNames[i] << ","; // Namen mit Komma trennen
        }
        else {
            Values_Names_for_csv << valueNames[i]; // Letzten Namen ohne Komma hinzufügen
            break;
        }
    }
    Values_Names_for_csv << std::endl; // Zeilenumbruch nach den Namen

    // Zusammenführen der Namen und Werte in allValues
    allValues << Values_Names_for_csv.str() << Values_for_csv.str();

    std::string writeFileName = "preset_number_" + selectFileNumber + ".csv"; // Dateiname mit der ausgewählten Nummer
    std::string filePath = ofToDataPath(writeFileName); // Pfad zur Datei

    bool fileExists = std::filesystem::exists(filePath); // Überprüfen, ob die Datei existiert

    std::ofstream outFile;
    if (fileExists) {
        // Wenn die Datei existiert, öffnen im Anhangsmodus
        outFile.open(filePath, std::ios_base::app);
        if (outFile.is_open()) {
            outFile << Values_for_csv.str(); // Werte anhängen
            outFile.close(); // Datei schließen
        }
        else {
            std::cerr << "Unable to open file for appending: " << writeFileName << std::endl; // Fehler beim Öffnen zum Anhängen
        }
    }
    else {
        // Wenn die Datei nicht existiert, neu erstellen
        outFile.open(filePath);
        if (outFile.is_open()) {
            // Kopfzeilen hinzufügen
            outFile << Values_Names_for_csv.str();
            // Werte hinzufügen
            outFile << Values_for_csv.str();
            outFile.close(); // Datei schließen
        }
        else {
            std::cerr << "Unable to create file: " << writeFileName << std::endl; // Fehler beim Erstellen der Datei
        }
    }
}

    

void ofApp::readValuesFromFile(const std::string& selectFileNumber)
{
    std::string fileValues = {};

    std::string readFileName = "preset_number_" + selectFileNumber;
    mGuiFileIO.read(ofToDataPath(readFileName), fileValues);

    const char delimiter = ' ';
    std::vector<std::string> outputArray;
    std::istringstream streamData(fileValues);
    std::string token;

    while (std::getline(streamData, token, delimiter))
    {
        token.erase(std::remove(token.begin(), token.end(), '\n'), token.end());
        outputArray.push_back(token);
    }

    for (int i = 0; i < outputArray.size() - 1; i += 2)
    {
        std::cout << outputArray[i] << " " << std::stof(outputArray[i + 1]) << std::endl;
    }
}