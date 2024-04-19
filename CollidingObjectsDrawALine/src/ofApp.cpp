#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup()
{
	ofBackground(ofColor(255));
}

//--------------------------------------------------------------
void ofApp::update()
{
	
}

//--------------------------------------------------------------
void ofApp::draw()
{
	ofSetColor(0, 0, 0);
	ofFill();

	if (mouseLeftPressedOnce == false)
	{
		ofDrawLine(lineStartPosition, glm::vec2(ofGetMouseX(), ofGetMouseY()));
	}

	for (int i = 0; i < lines.size(); i++)
	{
		lines[i].draw();
	}

	ofDrawBitmapString("Drag  Left  Mouse  Button  to  Draw  Lines", ofGetWidth() - 460, ofGetHeight() - 75);
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key)
{

}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button)
{
//	lineStartPosition = glm::vec2(ofGetMouseX(), ofGetMouseY()); 
}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button)
{ 
	if (button == 0)
	{
		lineStartPosition = glm::vec2(ofGetMouseX(), ofGetMouseY());

		mouseLeftPressedOnce = false;
	}
}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button)
{
	if (button == 0)
	{
		lineEndPosition = glm::vec2(x, y);
		lines.push_back(drawLine(lineStartPosition, lineEndPosition, ofColor(0, 0, 0)));

		mouseLeftPressedOnce = true;
	}

	NUMBER_OF_LINES = lines.size();
	std::cout << NUMBER_OF_LINES << std::endl;
}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
