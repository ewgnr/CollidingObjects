#pragma once

#include "ofMain.h"

class noiseGenerator
{
public:
	noiseGenerator() {}

	inline float play()
	{
		return ofRandom(-1, 1);
	}
};
