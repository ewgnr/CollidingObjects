#pragma once
#include "ofMain.h"

class drawLine
{
public:
	drawLine(const glm::vec2& pStartPos, const glm::vec2& pEndPos, const ofColor& pColor) : startPos(pStartPos), endPos(pEndPos), color(pColor) {}

	void draw()
	{
		ofSetLineWidth(2.0);
		ofSetColor(color);
		ofFill();
		ofDrawLine(startPos, endPos);
	}

	glm::vec2 startPos, endPos;
	ofColor color;
};