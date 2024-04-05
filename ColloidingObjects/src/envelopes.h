#pragma once

#include "ofMain.h"
#include <iostream>

class evelopeGenerator
{
public:
	evelopeGenerator(const float& pTimeCount) : index(0), phase(0), lifeTime(true), stopTimeInSeconds(pTimeCount) 
	{
		startTimeStamp = clock();
	}
	~evelopeGenerator() {}

	inline float play(const std::vector<float>& pBreakpoints)
	{
		if (pBreakpoints[index] < pBreakpoints[index + 1])
		{
			phase += (pBreakpoints[index + 1] - pBreakpoints[index]) / 44100 / (1 / pBreakpoints[index + 2]);

			if (phase >= pBreakpoints[index + 1])
			{
				index += 3;
			}
		}

		if (pBreakpoints[index] > pBreakpoints[index + 1])
		{
			phase += (pBreakpoints[index + 1] - pBreakpoints[index]) / 44100 / (1 / pBreakpoints[index + 2]);

			if (phase <= pBreakpoints[index + 1])
			{
				index += 3;
			}
		}

		if (index >= pBreakpoints.size() - 1)
		{
			phase = pBreakpoints[pBreakpoints.size() - 2];
		}

		if ((clock() - startTimeStamp) / CLOCKS_PER_SEC > stopTimeInSeconds)
		{
			lifeTime = false;
		}

		return phase;
	}

	inline bool isAlive()
	{
		return lifeTime;
	}

	bool lifeTime;

private:
	float phase, stopTimeInSeconds;
	size_t index;
	clock_t startTimeStamp;
};