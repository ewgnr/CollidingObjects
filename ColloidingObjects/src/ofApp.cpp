#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup() 
{
	ofBackground(ofColor(255));

	setSoundSettingsBasedOnOS();

	MAX_LINE_LENGTH = std::sqrt(ofGetWidth() * ofGetWidth() + ofGetHeight() * ofGetHeight());

	setupFinish();
}

//--------------------------------------------------------------
void ofApp::setupFinish()
{

	finishPositions.push_back(generateFinishPosition(minMarginToEdge));

	while (finishPositions.size() != 10)
	{
		if (finishPositions.size() == 0)
		{
			glm::vec2 temp_pos_1 = generateFinishPosition(minMarginToEdge);
			finishPositions.push_back(glm::vec2(temp_pos_1));
			std::cout << temp_pos_1.x << " " << temp_pos_1.y << std::endl;
		}

		glm::vec2 temp_pos_2 = generateFinishPosition(minMarginToEdge);
		glm::vec2 randomPos = glm::vec2(temp_pos_2);
		std::cout << temp_pos_2.x << " " << temp_pos_2.y << std::endl;

		bool inRange = false;
		for (int i = 0; i < finishPositions.size(); i++)
		{
			float dist_x = finishPositions[i].x - randomPos.x;
			float dist_y = finishPositions[i].y - randomPos.y;
			float distance = std::sqrt(dist_x * dist_x + dist_y * dist_y);

			if (distance <= finishRadius * 2)
			{
				inRange = true;
				break;
			}
		}

		if (!inRange)
		{
			finishPositions.push_back(randomPos);
		}
	}

	if (finishPositions.size() == 10)
	{
		for (int i = 0; i < finishPositions.size(); i++)
		{
			// std::cout << "true" << finishPositions[i].x << " " << finishPositions[i].y << std::endl;
			finishes.push_back(drawFinish(finishPositions[i], 270, ofRandom(360), finishRadius));
		}
	}

	for (int i = 0; i < finishes.size(); i++) {
		if (finishes[i].line.size() >= 2) {
			for (int j = 0; j < finishes[i].line.size() - 1; j++) {
				lines.push_back(drawLine(finishes[i].line[j], finishes[i].line[j + 1], ofColor(255, 0, 0)));
			}
		}
	}
}

//--------------------------------------------------------------
void ofApp::update()
{

	for (int i = balls.size() - 1; i >= 0; i--)
	{
		balls[i].update(balls, lines);

		if (balls[i].location.x - balls[i].radius < 0 || balls[i].location.x + balls[i].radius > ofGetWidth() || balls[i].location.y + balls[i].radius > ofGetHeight() || balls[i].isExpired)
		{
			balls.erase(balls.begin() + i);
		}

		if (balls[i].collideLines)
		{
			float frequency_unclipped = ((1-(balls[i].lineCircleProperies / MAX_LINE_LENGTH)) * (1-(balls[i].radius / MAX_BALL_RADIUS) * 0.5 * SPREAD));
			frequency = std::max(0.0f, std::min(frequency_unclipped, 1.0f)) * MAX_FREQ_RANGE + MAX_FREQ_OFFSET;
			audioTriggerLines = true;
			balls[i].collideLines = false;
		}

		if (collideTest)
		{
			audioTriggerTest = true;
			collideTest = false;
		}
	}
	teleportBalls();
}

//--------------------------------------------------------------
void ofApp::draw()
{

	for (int i = 0; i < finishes.size(); i++)
	{
		finishes[i].draw();
	}
    
    for (int i = 0; i < balls.size(); i++)
	{
		balls[i].draw();
	}
	
	for (int i = 0; i < lines.size(); i++)
	{
		lines[i].draw();
	}

	if (mouseLeftPressedOnce == false)
	{
		ofSetLineWidth(2.0);
		ofSetColor(0, 0, 0);
		ofFill();
		ofDrawLine(lineStartPosition, glm::vec2(ofGetMouseX(), ofGetMouseY()));
	}

	if (mouseRightPressedOnce == false)
	{
		linesize = glm::vec2(ofGetMouseX(), ofGetMouseY());

		float dist_x = calcDirStart.x - linesize.x;
		float dist_y = calcDirStart.y - linesize.y;

		float angle = std::atan2(dist_y, dist_x);
		double degree = angle * (180.0 / PI);

		int len = sqrt(((dist_x * dist_x) + (dist_y * dist_y)));

		statbox = "Angle: " + to_string(static_cast<int>(degree * -1)) + "\u00B0" + "\nLength: " + to_string(static_cast<int>(len)) + "px";

		ofSetLineWidth(2.0);
		ofSetColor(155, 0, 0);
		ofFill();
		ofDrawLine(calcDirStart, glm::vec2(ofGetMouseX(), ofGetMouseY()));
		ofSetColor(0);
		ofDrawBitmapString(statbox, ofGetMouseX() + 25, ofGetMouseY() - 25);
	}

	ofSetColor(0, 0, 0);
	ofFill();
	ofDrawBitmapString("Drag    Left    Mouse    Button    to    Draw    Lines", ofGetWidth() - 460, ofGetHeight() - 75);
	ofDrawBitmapString("Press   Mouse   Weel     to       Reset     Everything", ofGetWidth() - 460, ofGetHeight() - 50);
	ofDrawBitmapString("Drag Right Mouse Button to Generate a Colliding Object", ofGetWidth() - 460, ofGetHeight() - 25);

	if (finishPositions.size() == 10)
	{
		for (int i = 0; i < finishPositions.size(); i++)
		{
			ofSetColor(0, 0, 255);
			ofFill();
			ofDrawCircle(finishPositions[i], 10);
		}
	}
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key)
{
	if (key == ' ')
	{
		audioTriggerTest = true;
	}

	if (key == 's')
	{
		ofImage img;
		img.grabScreen(0, 0, ofGetWidth(), ofGetHeight());
		ofSaveImage(img, "mySnapshot.png");
	}
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key)
{
}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button)
{
	if (button == 0 && mouseLeftPressedOnce)
	{
		lineStartPosition = glm::vec2(ofGetMouseX(), ofGetMouseY());
		mouseLeftPressedOnce = false;
	} 

	if (button == 1)
	{
		lines.clear();
		finishes.clear();
		finishPositions.clear();
		setupFinish();
	}

	if (button == 2 && mouseRightPressedOnce)
	{
		calcDirStart = glm::vec2(ofGetMouseX(), ofGetMouseY());
		mouseRightPressedOnce = false;
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

	if (button == 2)
	{
		calcDirEnd = linesize;

		float dist_x = calcDirStart.x - calcDirEnd.x;
		float dist_y = calcDirStart.y - calcDirEnd.y;

		float lineLength = std::sqrt((dist_x * dist_x) + (dist_y * dist_y));

		float angle = std::atan2(dist_y, dist_x);
		float dx = std::cos(angle);
		float dy = std::sin(angle);

		bool blockBallCreation = false;
		for (int lI = 0; lI < lines.size(); lI++)
		{
			if (lineCircle(lines[lI], calcDirStart, glm::vec2(dx, dy), (lineLength / MAX_LINE_LENGTH) * MAX_BALL_RADIUS))
			{
				blockBallCreation = true;
			}
		}
		if (!blockBallCreation)
			balls.push_back(Ball(calcDirStart, 255, (lineLength / MAX_LINE_LENGTH) * MAX_BALL_RADIUS, MAX_BALL_RADIUS, glm::vec2(dx, dy), GRAVITY));

		mouseRightPressedOnce = true;
	}
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

//--------------------------------------------------------------
void ofApp::audioOut(ofSoundBuffer& buffer)
{
	std::vector<float> envParam_1 = { 0, 1, 100,  1, 0, 100 };
	std::vector<float> envParam_2 = { 0, 1, 10,    1, 0, 10   };

	if (audioTriggerLines)
	{		
		frequencies.push_back(frequency);
		modes.push_back(std::make_shared<modalFilter>());
		noises.push_back(std::make_shared<noiseGenerator>());
		envelopes.push_back(std::make_shared<evelopeGenerator>(2.0f));

		audioTriggerLines = false;
	}

	if (audioTriggerTest)
	{
		testNoise.push_back(std::make_shared<noiseGenerator>());
		testEnv.push_back(std::make_shared<evelopeGenerator>(2.0f));

		audioTriggerTest = false;
	}

	for (int mI = modes.size() - 1; mI >= 0; mI--)
	{
		modes[mI]->init(frequencies[mI], frequencies[mI] * 2.0, 1.0);
	}

	for (int sample = 0; sample < buffer.size(); sample++)
	{
		for (int mI = envelopes.size() - 1; mI >= 0; mI--)
		{
			output += modes[mI]->play(noises[mI]->play() * envelopes[mI]->play(envParam_1)) * 0.001;

			if (envelopes[mI]->isAlive() == false && envelopes.size() != 0 && modes.size() != 0 && noises.size() != 0 && frequencies.size() != 0)
			{
				modes.erase(modes.begin());
				noises.erase(noises.begin());
				envelopes.erase(envelopes.begin());
				frequencies.erase(frequencies.begin());
			}
		}

		for (int mI = testEnv.size() - 1; mI >= 0; mI--)
		{
			testOutput += testNoise[mI]->play() * testEnv[mI]->play(envParam_2) * 0.001;
		}

		buffer[sample] = output + testOutput;
		output = 0;
		testOutput = 0;
	}
}

