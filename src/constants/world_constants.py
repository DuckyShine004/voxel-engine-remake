CHUNK_SIZE = 32
WORLD_WIDTH = 4
WORLD_HEIGHT = 4
WORLD_DEPTH = 4

VERTICES = [
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 0.0],
]

# ORDER: TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT
INDICES = [
    [4, 5, 6],
    [4, 6, 7],
    [1, 0, 3],
    [1, 3, 2],
    [5, 1, 2],
    [5, 2, 6],
    [4, 3, 0],
    [4, 7, 3],
    [4, 0, 1],
    [4, 1, 5],
    [7, 6, 2],
    [7, 2, 3],
]

NOISE_FACTOR = 10.0
NOISE_AMPLITUDE = 25.0
NOISE_OCTAVES = 4
NOISE_PERSISTENCE = 0.3
NOISE_EXPONENT = 0.9

TEXTURE_WIDTH = 16
TEXTURE_HEIGHT = 48

BLOCK_TYPES = {
    "air": 0,
    "stone": 1,
    "grass": 2,
    "dirt": 3,
}
