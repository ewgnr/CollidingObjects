#pragma once
#include "ofMain.h"
#include "Line.h"

inline bool pointCircle(glm::vec2 pPoint, glm::vec2 pLocation, float pRadius)
{
	float dist_x = pPoint.x - pLocation.x;
	float dist_y = pPoint.y - pLocation.y;

	float distance = std::sqrt((dist_x * dist_x) + (dist_y * dist_y));

	if (distance <= pRadius)
	{
		return true;
	}
	return false;
}

inline bool linePoint(drawLine pLine, glm::vec2 pLocation)
{
	float d1 = glm::distance(pLocation, pLine.startPos);
	float d2 = glm::distance(pLocation, pLine.endPos);

	float lineLength = glm::distance(pLine.startPos, pLine.endPos);

	if (d1 + d2 >= lineLength - 0.1 && d1 + d2 <= lineLength + 0.1)
	{
		return true;
	}
	return false;
}

inline float calculateLineLength(drawLine pLine)
{
	float dist_x = pLine.startPos.x - pLine.endPos.x;
	float dist_y = pLine.startPos.y - pLine.endPos.y;
	return sqrt((dist_x * dist_x) + (dist_y * dist_y));
}

inline glm::vec2 calculateClosest(drawLine pLine, glm::vec2 pLocation)
{
	float lineLength = calculateLineLength(pLine);

	float dot = (((pLocation.x - pLine.startPos.x) * (pLine.endPos.x - pLine.startPos.x)) + ((pLocation.y - pLine.startPos.y) * (pLine.endPos.y - pLine.startPos.y))) / std::pow(lineLength, 2);

	float closest_x = pLine.startPos.x + (dot * (pLine.endPos.x - pLine.startPos.x));
	float closest_y = pLine.startPos.y + (dot * (pLine.endPos.y - pLine.startPos.y));

	return glm::vec2(closest_x, closest_y);
}

inline float lineCircleDistance(glm::vec2 pClosest, glm::vec2 pLocation)
{
	float dist_x = pClosest.x - pLocation.x;
	float dist_y = pClosest.y - pLocation.y;

	return std::sqrt((dist_x * dist_x) + (dist_y * dist_y));
}

inline bool lineCircle(drawLine pLine, glm::vec2 pLocation, glm::vec2 pVelocity, float pRadius)
{
	glm::vec2 closest = calculateClosest(pLine, pLocation);

	bool on_segment = linePoint(pLine, closest);
	if (!on_segment) return false;

	if (lineCircleDistance(closest, pLocation) <= pRadius)
	{
		return true;
	}
	return false;
}
