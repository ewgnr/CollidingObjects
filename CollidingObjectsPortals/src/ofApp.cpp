// https://gamedev.stackexchange.com/questions/20202/collision-with-half-of-a-semi-circle

#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){

}

//--------------------------------------------------------------
void ofApp::update()
{   
    glm::vec2 Earth = glm::vec2(ofGetWidth() / 2, ofGetHeight() / 2); 
    glm::vec2 Meteor = glm::vec2(ofGetMouseX(), ofGetMouseY());

    distance = glm::distance(Earth, Meteor);

    if (distance < radians + thickness && distance > radians - thickness)
    {
        float dist_x = Meteor.x - Earth.x;
        float dist_y = Meteor.y - Earth.y;
        float angle = glm::atan(dist_y, dist_x);
        float degree = glm::degrees(angle) + 180;

        if (degree > 0 && degree < 45)
        {
            std::cout << "pass" << std::endl;
        }
        else
        {
            if (distance < radians)
            {
                std::cout << "hit" << std::endl;
            }
        }
    }
}
//--------------------------------------------------------------
void ofApp::draw()
{
    ofSetLineWidth(thickness);
    ofNoFill();
    ofSetColor(0, 0, 0);
    ofDrawCircle(glm::vec2(ofGetWidth()/2,ofGetHeight()/2), radians);
    
    ofSetColor(100, 0, 0);
    ofDrawCircle(glm::vec2(ofGetMouseX(),ofGetMouseY()), 2);
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){

}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

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
