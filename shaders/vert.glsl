#version 330 core

layout (location = 0) in vec3 mGlobalPos;
layout (location = 3) in vec3 mObjectPos;

void main() {
    vec3 mLocalPos = mGlobalPos + mObjectPos;

    gl_Position = vec4(mLocalPos, 1.0);
}
