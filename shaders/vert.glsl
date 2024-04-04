#version 330 core

layout (location = 0) in vec3 mGlobalPos;
layout (location = 3) in vec3 mObjectPos;

uniform mat4 mProjectionView;

void main() {
    vec3 mLocalPos = mGlobalPos + mObjectPos;

    gl_Position = mProjectionView * vec4(mLocalPos, 1.0);
}
