#pragma once

// https://processing.org/examples/circlecollision.html
// https://github.com/processing/processing/blob/master/core/src/processing/core/PVector.java

#include "ofMain.h"
#include <glm/gtc/random.hpp> 


class ball
{
public:
	ball(const float& pX, const float& pY, const float& pRadius) : position(glm::vec2(pX, pY)), velocity(glm::vec2(glm::linearRand<float>(-1, 1), glm::linearRand<float>(-1, 1))), radius(pRadius), mass(pRadius * 0.1) {}

	void update()
	{
		position = position += (velocity * 10);
	}

	void checkBoundaryCollision() 
	{
		if (position.x > ofGetWidth() - radius) 
		{
			position.x = ofGetWidth() - radius;
			velocity.x *= -1;
		}
		else if (position.x < radius) 
		{
			position.x = radius;
			velocity.x *= -1;
		}
		else if (position.y > ofGetHeight() - radius)
		{
			position.y = ofGetHeight() - radius;
			velocity.y *= -1;
		}
		else if (position.y < radius) 
		{
			position.y = radius;
			velocity.y *= -1;
		}
	}

	void checkCollision(ball& pOther)
	{
		glm::vec2 distanceVect = pOther.position - position;
		float distanceVectMag = glm::length(distanceVect);
		float minDistance = radius + pOther.radius;

		if (distanceVectMag < minDistance) 
		{
			float distanceCorrection = (minDistance - distanceVectMag) / 2.0f;

			glm::vec2 d = distanceVect;
			glm::vec2 correctionVector = glm::normalize(d) *= distanceCorrection;

			pOther.position = pOther.position += correctionVector;
			position = position -= correctionVector;

			float theta = glm::atan(distanceVect.y, distanceVect.x);
			float sine = glm::sin(theta);
			float cosine = glm::cos(theta);

			std::array<glm::vec2, 2> bTemp;
			
			bTemp[1].x = cosine * distanceVect.x + sine * distanceVect.y;
			bTemp[1].y = cosine * distanceVect.y - sine * distanceVect.x;

			std::array<glm::vec2, 2> vTemp;

			vTemp[0].x = cosine * velocity.x + sine * velocity.y;
			vTemp[0].y = cosine * velocity.y - sine * velocity.x;
			vTemp[1].x = cosine * pOther.velocity.x + sine * pOther.velocity.y;
			vTemp[1].y = cosine * pOther.velocity.y - sine * pOther.velocity.x;

			std::array<glm::vec2, 2> vFinal;

			vFinal[0].x = ((mass - pOther.mass) * vTemp[0].x + 2.0f * pOther.mass * vTemp[1].x) / (mass + pOther.mass);
			vFinal[0].y = vTemp[0].y;

			vFinal[1].x = ((pOther.mass - mass) * vTemp[1].x + 2.0f * mass * vTemp[0].x) / (mass + pOther.mass);
			vFinal[1].y = vTemp[1].y;

			bTemp[0].x += vFinal[0].x;
			bTemp[1].x += vFinal[1].x;

			std:array<glm::vec2, 2> bFinal;

			bFinal[0].x = cosine * bTemp[0].x - sine * bTemp[0].y;
			bFinal[0].y = cosine * bTemp[0].y + sine * bTemp[0].x;
			bFinal[1].x = cosine * bTemp[1].x - sine * bTemp[1].y;
			bFinal[1].y = cosine * bTemp[1].y + sine * bTemp[1].x;

			pOther.position.x = position.x + bFinal[1].x;
			pOther.position.y = position.y + bFinal[1].y;

			position = position += bFinal[0];

			velocity.x = cosine * vFinal[0].x - sine * vFinal[0].y;
			velocity.y = cosine * vFinal[0].y + sine * vFinal[0].x;
			pOther.velocity.x = cosine * vFinal[1].x - sine * vFinal[1].y;
			pOther.velocity.y = cosine * vFinal[1].y + sine * vFinal[1].x;
		}
	}

	void display() 
	{
		ofSetColor(255);
		ofFill();
		ofDrawEllipse(position.x, position.y, radius * 2, radius * 2);
	}

	glm::vec2 position, velocity;
	float radius, mass;
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
		
		std::array<ball, 2> balls = { ball(100, 400, 40), ball(700, 400, 80) };
};
