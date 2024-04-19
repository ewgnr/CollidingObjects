#include "ofApp.h"

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
    std::ostringstream allValues;

    for (int i = 0; i < valueNames.size(); ++i)
    {
        std::cout << valueNames[i] << " " << values[i] << " " << std::endl;
        allValues << valueNames[i] << " " << values[i] << " " << std::endl;
    }

    std::string writeFileName = "preset_number_" + selectFileNumber;
    mGuiFileIO.write(allValues.str(), ofToDataPath(writeFileName));
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