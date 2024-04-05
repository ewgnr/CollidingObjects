#pragma once
#include "ofMain.h"
#include "Line.h"
#include "collisions.h"

class Ball
{
public:
	Ball(const glm::vec2& pPos, const float& pAlpha, const float& pRadius, const float& pMAX_BALL_RADIUS, const glm::vec2& pVelocity, const glm::vec2& pGravity) : location(pPos), alpha(pAlpha), velocity(pVelocity), gravity(pGravity), radius(pRadius), MAX_BALL_RADIUS(pMAX_BALL_RADIUS), collideLines(false), lineCircleProperies(0), lifetime(pAlpha), isExpired(false) {}

	void update(std::vector<Ball> pBalls, std::vector<drawLine> pLines)
	{
		tempLocation = location;

		location += velocity;
		velocity += gravity;

		float weight = 1 - (radius / MAX_BALL_RADIUS);
		location += velocity *= weight;
		lifetime -= weight * 0.1;

		for (int bI = pBalls.size() - 1; bI >= 0; bI--)
		{
			float dist_x = pBalls[bI].location.x - location.x;
			float dist_y = pBalls[bI].location.y - location.y;
			float distance = (std::sqrt(dist_x * dist_x + dist_y * dist_y));
			float min_dist = pBalls[bI].radius + radius;

			if (distance <= min_dist)
			{
				float angle = std::atan2(dist_y, dist_x);
				float tx = location.x + std::cos(angle) * min_dist;
				float ty = location.y + std::sin(angle) * min_dist;
				float ax = (tx - pBalls[bI].location.x) * 0.01;
				float ay = (ty - pBalls[bI].location.y) * 0.01;

				velocity.x -= ax;
				velocity.y -= ay;

				pBalls[bI].velocity.x += ax;
				pBalls[bI].velocity.x += ay;
			}
		}
		// https://www.jeffreythompson.org/collision-detection/line-circle.php
		for (int lI = pLines.size() - 1; lI >= 0; lI--)
		{
			if (lineCircle(pLines[lI], location, velocity, radius))
			{
				location = tempLocation;

				glm::vec2 baseDelta = pLines[lI].startPos - pLines[lI].endPos;
				baseDelta = glm::normalize(baseDelta);
				glm::vec2 normal = glm::vec2(-baseDelta.y, baseDelta.x);

				glm::vec2 incidence = velocity * -1;
				incidence = glm::normalize(incidence);

				float dot = glm::dot(incidence, normal);
				velocity = glm::vec2(2 * normal.x * dot - incidence.x, 2 * normal.y * dot - incidence.y);

				lineCircleProperies = calculateLineLength(pLines[lI]);

				collideLines = true;
			}

			if (pointCircle(pLines[lI].startPos, location, radius) || pointCircle(pLines[lI].endPos, location, radius) && !lineCircle(pLines[lI], location, velocity, radius))
			{
				location = tempLocation;

				velocity *= -1;

				collideLines = true;
			}

			if (lifetime <= 0)
			{
				isExpired = true;
			}
		}
	}

	void draw()
	{
		ofSetColor(0, 0, 0, lifetime);
		ofFill();
		ofDrawCircle(location, radius);
	}

	bool isExpired;

	float lineCircleProperies;
	bool collideLines;

	float MAX_BALL_RADIUS;
	float radius;
	glm::vec2 location, velocity;

private:
	float alpha, lifetime;
	glm::vec2 velocityOld;
	glm::vec2 gravity;
	glm::vec2 tempLocation;
};