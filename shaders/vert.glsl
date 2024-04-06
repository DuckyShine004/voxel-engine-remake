#version 330 core

layout (location = 0) in vec3 mGlobalPos;
layout (location = 1) in vec2 mObjectTexCoords;
layout (location = 2) in float mObjectTexIndex;
layout (location = 3) in vec3 mObjectPos;

uniform mat4 mProjectionView;

out vec2 fObjectTexCoords;
out float fObjectTexIndex;

void main() {
    vec3 mLocalPos = mGlobalPos + mObjectPos;

    gl_Position = mProjectionView * vec4(mLocalPos, 1.0);

    fObjectTexCoords = mObjectTexCoords;
    fObjectTexIndex = mObjectTexIndex;
}
