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

float calculateLineLength(const glm::vec2& mMouseCoordinateStart, const glm::vec2& mMouseCoordinateEnd)
{
	float dist_x = mMouseCoordinateStart.x - mMouseCoordinateEnd.x;
	float dist_y = mMouseCoordinateStart.y - mMouseCoordinateEnd.y;

	return sqrt(((dist_x * dist_x) + (dist_y * dist_y)));
}

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

		bool mouseLeftPressedOnce = true;
		std::size_t NUMBER_OF_LINES;
};
