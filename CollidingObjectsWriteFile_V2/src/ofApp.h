/*
For a socket based solutions (osc) : \of_v0.12.0_vs_release\addons\ofxOSC
A shared memory solution : https://www.boost.org/doc/libs/1_54_0/doc/html/interprocess/sharedmemorybetweenprocesses.html
(Check how to implement in OF)
*/

#pragma once

#include "ofMain.h"
#include <iostream>
#include <fstream>
#include <sstream>

class fileIO
{
public:
	fileIO() {}

	void read(const std::string& pFileName, std::string& pString)
	{
		std::ifstream fileStream(pFileName.c_str());
		std::stringstream ss;
		ss << fileStream.rdbuf();
		pString = ss.str();
	}

	void write(const std::string& pString, const std::string& pFileName)
	{
		std::ofstream fileStream(pFileName.c_str());
		fileStream << pString;
		fileStream.close();
	}
};

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void saveValuesAsFile(const std::string& selectFileNumber);
		void readValuesFromFile(const std::string& selectFileNumber);

		fileIO mGuiFileIO;

		std::vector<string> valueNames =
		{
			"NUMBER_OF_COLLISIONS",
			"NUMBER_OF_BALLS",
			"NUMBER_OF_LINES",
			"NUMBER_OF_TELEPORTS",
			"NUMBER_OF_FAILS",
			"HARMONICITY",
			"PLAY_DURATION"
		};

		std::vector<float> values = { 1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f };
};
