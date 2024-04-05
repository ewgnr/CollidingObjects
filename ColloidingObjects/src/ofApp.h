#pragma once

#include "ofMain.h"
#include "Ball.h"
#include "Line.h"
#include "Collisions.h"
#include "modalFilter.h"
#include "envelopes.h"
#include "noise.h"
#include "Finish.h"

class ofApp : public ofBaseApp{

	public:
		void setup();
        void setupFinish();
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
		void audioOut(ofSoundBuffer& buffer);

		float MAX_LINE_LENGTH;
		float MAX_BALL_RADIUS = 160;

        glm::vec2 GRAVITY = glm::vec2(0.0, 0.01);

		std::vector<Ball> balls;
		glm::vec2 lineStartPosition, lineEndPosition;
		std::vector<drawLine> lines;
    
		glm::vec2 calcDirStart, calcDirEnd;
		bool mouseLeftPressedOnce = true;
		bool mouseRightPressedOnce = true;

		bool audioTriggerLines;
        bool audioTriggerTest;

		float MAX_FREQ_OFFSET = 100;
		float MAX_FREQ_RANGE = 1000;
        float SPREAD = 5;

		ofSoundStream soundStream;
		float frequency;
		std::vector<float> frequencies;
		std::vector<std::shared_ptr<modalFilter>> modes;
		std::vector<std::shared_ptr<evelopeGenerator>> envelopes;
		std::vector<std::shared_ptr<noiseGenerator>> noises;
		float output;
    
    void setSoundSettingsBasedOnOS(){
        ofSoundStreamSettings settings;
        
        #ifdef _WIN32

            settings.setApi(ofSoundDevice::Api::MS_DS);
            auto devices = soundStream.getDeviceList(ofSoundDevice::Api::MS_DS);

        #elif __APPLE__

            settings.setApi(ofSoundDevice::Api::OSX_CORE);
            auto devices = soundStream.getDeviceList(ofSoundDevice::Api::OSX_CORE);

        #elif __linux__

            settings.setApi(ofSoundDevice::Api::OSS);
            auto devices = soundStream.getDeviceList(ofSoundDevice::Api::OSS);

        #else

            settings.setApi(ofSoundDevice::Api::UNSPECIFIED);
            auto devices = soundStream.getDeviceList(ofSoundDevice::Api::UNSPECIFIED);

        #endif
        for (int i = 0; i < devices.size(); i++) {
            std::cout << devices[i] << "\n";
        }
        
        settings.setOutDevice(devices[0]);
        settings.setOutListener(this);
        settings.numOutputChannels = 1;
        settings.sampleRate = 44100;
        settings.bufferSize = 1024;
        settings.numBuffers = 4;
        soundStream.setup(settings);
    }
    
    float finishRadius = 50;
    float minMarginToEdge = 100;
    std::vector<drawFinish> finishes;
    std::vector<glm::vec2> finishPositions;

    glm::vec2 generateFinishPosition(const float& pMinMarginToEdge)
    {
        return glm::vec2(ofRandom(pMinMarginToEdge, ofGetWindowWidth() - pMinMarginToEdge), ofRandom(pMinMarginToEdge, ofGetWindowHeight() - pMinMarginToEdge));
    }

    void teleportBalls() {

        for (int i = 0; i < finishes.size(); i++)
        {

            int indexOfNextFinish = 0;
            if (i == finishes.size() - 1) {
                indexOfNextFinish = 0;
            }
            else
            {
                indexOfNextFinish = i + 1;
            }

            for (int j = 0; j < balls.size(); j++)
            {
                float distanceToFinish = glm::distance(balls[j].location, finishes[i].getPos());

                if (distanceToFinish <= finishes[i].getRadius())
                {
                    setNewLocation(balls[j].location, finishes[indexOfNextFinish]);
                    setAndAddNewVelocity(balls[j].velocity, finishes[indexOfNextFinish].getPos(), balls[j].location);
                }
            }

        }
    }

    void setAndAddNewVelocity(glm::vec2& velocity, glm::vec2 center, glm::vec2& location) {

        glm::vec2 normal = glm::normalize(location - center);
        float velocityMagnitude = glm::length(velocity);
        velocity = normal * velocityMagnitude;
        location += velocity;
    }

    void setNewLocation(glm::vec2& location, drawFinish nextFinish) {

        glm::vec2 centerOfNextFinish = nextFinish.getPos();
        float gapMiddleDegreesOfNextFinish = nextFinish.getRotation() + nextFinish.getDegrees() + (360 - nextFinish.getDegrees()) / 2;
        float gapMiddleRadOfNextFinish = ofDegToRad(gapMiddleDegreesOfNextFinish);
        float x = centerOfNextFinish.x + nextFinish.getRadius() * cos(gapMiddleRadOfNextFinish);
        float y = centerOfNextFinish.y + nextFinish.getRadius() * sin(gapMiddleRadOfNextFinish);
        glm::vec2 centerOfGapOfNextFinish = glm::vec2(x, y);
        location = centerOfGapOfNextFinish;
    }

    double degree;
    float len;
    glm::vec2 linesize;
    std::string statbox;

    bool collideTest;
    std::vector<std::shared_ptr<evelopeGenerator>> testEnv;
    std::vector<std::shared_ptr<noiseGenerator>> testNoise;
    float testOutput;
};
