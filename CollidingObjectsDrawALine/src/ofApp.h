#pragma once

#include "ofMain.h"

/*
BUG FIXES: See main code for drawing line by pressing the right mouse button.
Adapt the following behaviour to this code: 
1. Drawing a preview of the line, before the mouse button is released.
2. Drawing a bitmap string, containing the legth in pixels of the line.
*/

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

class ofApp : public ofBaseApp
{
	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void mouseEntered(int x, int y);
		void mouseExited(int x, int y);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
		
		glm::vec2 lineStartPosition, lineEndPosition;
		std::vector<drawLine> lines;
};
