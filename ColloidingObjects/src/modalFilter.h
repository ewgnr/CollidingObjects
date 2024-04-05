#pragma once

#include "ofMain.h"

class modalFilter
{
public:
	modalFilter() : x1(0), y1(0), y2(0), alpha(0), beta(0), sum(0), frq(0), q(0), amp(0), out(0) {}

	void init(const float& pFrq, const float& pQ, const float& pAmp)
	{
		frq = pFrq;
		q = pQ;
		amp = pAmp;

		if (44100 / frq < PI)
		{
			std::cout << "This filter becomes unstable if sr/xfreq < pi (e.g xfreq > 14037 Hz @ 44 kHz)" << "\n";
			return;
		}

		frq = frq * 2 * PI;
		alpha = 44100 / frq;
		beta = alpha * alpha;
	}

	inline float play(const float& pIn)
	{
		x1 = pIn;
		sum = (-(1 - 2 * beta) * y1 + x1 - (beta - alpha / (2 * q)) * y2) / (beta + alpha / (2 * q));
		y2 = y1;
		y1 = sum;
		out = sum * 44100 / (2 * frq) * amp;
		return out;
	}

private:
	float x1, y1, y2, alpha, beta, sum, frq, q, amp, out;
};

