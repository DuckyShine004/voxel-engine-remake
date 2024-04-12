#version 330 core

layout (location = 0) in vec3 mGlobalPos;
layout (location = 1) in vec2 mObjectTexCoords;
layout (location = 2) in float mOpaqueTexIndex;
layout (location = 3) in float mTransparentTexIndex;
layout (location = 4) in vec3 mOpaqueObjectPos;
layout (location = 5) in vec3 mTransparentObjectPos;

uniform mat4 mProjectionView;
uniform int mIsTransparent;

out vec2 fObjectTexCoords;
out float fObjectTexIndex;
out vec3 fObjectPos;

void main() {
    vec3 localPos = mGlobalPos;

    if (mIsTransparent == 1) {
        localPos += mTransparentObjectPos;
        fObjectPos = mTransparentObjectPos;
        fObjectTexIndex = mTransparentTexIndex;
    } else {
        localPos += mOpaqueObjectPos;
        fObjectPos = mOpaqueObjectPos;
        fObjectTexIndex = mOpaqueTexIndex;
    }

    gl_Position = mProjectionView * vec4(localPos, 1.0);

    fObjectTexCoords = mObjectTexCoords;
}
