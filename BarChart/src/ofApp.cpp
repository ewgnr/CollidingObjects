#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    ofSetBackgroundColor(255, 255, 255);  
    infoText = "Info\nmin: rot\neigen: schwarz\nmax: blau";  

   
    minValues[0] = 100; myValues[0] = 300; maxValues[0] = 400;
    minValues[1] = 50;  myValues[1] = 200; maxValues[1] = 350;
    minValues[2] = 150; myValues[2] = 250; maxValues[2] = 450;
    minValues[3] = 120; myValues[3] = 270; maxValues[3] = 420;
    minValues[4] = 80;  myValues[4] = 260; maxValues[4] = 380;
    minValues[5] = 130; myValues[5] = 280; maxValues[5] = 430;
    minValues[6] = 90;  myValues[6] = 240; maxValues[6] = 370;

    verdana.load("verdana.ttf", 12, true, true);
    verdana.setLineHeight(20.0f);
    verdana.setLetterSpacing(1.035);
}

//--------------------------------------------------------------
void ofApp::update(){

}

//--------------------------------------------------------------
void ofApp::draw(){
	 float numGroups = 7; // Anzahl der Balkengruppen

    float totalWidth = ofGetWidth();
    float sidePadding = 20.0;
    float diagramWidth = totalWidth - 2 * sidePadding;
    float gapBetweenGroups = totalWidth * 0.05;
    float barGroupWidth = (diagramWidth - gapBetweenGroups * (numGroups - 1)) / numGroups;

    float barWidthMin = barGroupWidth * 0.2; // Breite für min-Balken (20%)
    float barWidthMy = barGroupWidth * 0.6;  // Breite für eigenen-Balken (60%)
    float barWidthMax = barGroupWidth * 0.2; // Breite für max-Balken (20%)

    float startY = ofGetHeight() - 30; // Abstand zum unteren Rand des Fensters
    float maxBarHeight = ofGetHeight() - 300; // Maximalhöhe der Balken über dem unteren Rand

    string groupNames[7] = { "COLLISIONS", "BALLS", "LINES", "TELEPORTS", "FAILS", "DURATION", "HARMONICITY" }; // Namen für die Balkengruppen

    ofSetColor(0); // Schwarz für die Textfarbe der Legende


 
    verdana.drawString(infoText, ofGetWidth() - 150, 50); // Schrift

    for (int i = 0; i < numGroups; i++) {
        float currentGroupStartX = sidePadding + i * (barGroupWidth + gapBetweenGroups);
        float barHeightMin = ofMap(minValues[i], 0, 500, 0, maxBarHeight);
        float barHeightMy = ofMap(myValues[i], 0, 500, 0, maxBarHeight);
        float barHeightMax = ofMap(maxValues[i], 0, 500, 0, maxBarHeight);

        // Zeichnen der Balken
        ofSetColor(255, 0, 0); // Rot für min-Werte
        ofDrawRectangle(currentGroupStartX, startY - barHeightMin, barWidthMin, barHeightMin);

        ofSetColor(0); // Schwarz für eigenen-Werte
        ofDrawRectangle(currentGroupStartX + barWidthMin, startY - barHeightMy, barWidthMy, barHeightMy);

        ofSetColor(0, 0, 255); // Blau für max-Werte
        ofDrawRectangle(currentGroupStartX + barWidthMin + barWidthMy, startY - barHeightMax, barWidthMax, barHeightMax);

       
        ofSetColor(0); // Schwarz
        float textWidth = barGroupWidth * 0.8; 
        verdana.drawString(groupNames[i], currentGroupStartX + (barGroupWidth - textWidth) / 2, startY + 20); // Schrift

    }
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
