#pragma once
#include "ofMain.h"
#include "ofPath.h"

class drawFinish
{
public:

    drawFinish(const glm::vec2& pPos, const int pDegrees, const int pRotation, const float pRadius) : pos(pPos), degrees(pDegrees), rotation(pRotation), radius(pRadius), color(ofColor(255, 0, 0))
    {
        for (int i = 0; i <= degrees; i++) {
            float rad = ofDegToRad(i + rotation);
            float x = pos.x + radius * cos(rad);
            float y = pos.y + radius * sin(rad);
            line.addVertex(ofPoint(x, y));
        }
    }

    void draw()
    {
        ofSetColor(color);
        ofSetLineWidth(5);
        line.draw();
    }

    glm::vec2 getPos() {
        return pos;
    }

    float getRadius() {
        return radius;
    }

    int getRotation() {
        return rotation;
    }

    int getDegrees() {
        return degrees;
    }

    ofPolyline line;
    float radius;

private:
    glm::vec2 pos;
    int degrees;
    int rotation;
    ofColor color;
};