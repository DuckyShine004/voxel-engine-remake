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

NOISE_OCTAVES = 6
NOISE_PERSISTENCE = 0.5
NOISE_LACUNARITY = 2.0
