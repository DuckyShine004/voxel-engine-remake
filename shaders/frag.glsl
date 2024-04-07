#version 330 core

in vec2 fObjectTexCoords;
in float fObjectTexIndex;

uniform vec3 mCameraPos;
uniform sampler2DArray mTextureArr;

out vec4 FragColor;

void main() {
    //FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    vec4 mTexColor = texture(mTextureArr, vec3(fObjectTexCoords, fObjectTexIndex));
    FragColor = mTexColor;
}
