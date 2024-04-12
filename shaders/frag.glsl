#version 330 core

in vec2 fObjectTexCoords;
in float fObjectTexIndex;
in vec3 fObjectPos;

uniform vec3 mCameraPos;
uniform float mFogStart;
uniform float mFogEnd;
uniform vec4 mFogColor;
uniform sampler2DArray mTextureArr;

out vec4 FragColor;

float getFog() {
    float fogDistance = length(fObjectPos - mCameraPos);

    return clamp((mFogStart - fogDistance) / (mFogEnd - mFogStart), 0.0, 1.0);
}

void main() {
    vec4 texColor = texture(mTextureArr, vec3(fObjectTexCoords, fObjectTexIndex));
    vec3 finalColor = mix(mFogColor.rgb, texColor.rgb, getFog());

    FragColor = vec4(finalColor, texColor.a);
}
