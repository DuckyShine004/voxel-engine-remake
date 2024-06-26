BACKGROUND_COLOR = (0.5, 0.7, 1.0, 1.0)

CHUNK_SIZE = 32
WORLD_WIDTH = 4
WORLD_HEIGHT = 4
WORLD_DEPTH = 4

FOG_START = 50.0
FOG_END = 100.0

# ORDER: TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT
VERTICES = [
    [0.0, 1.0, 0.0],
    [0.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 1.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
]

# ORDER: TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT
INDICES = [
    [0, 1, 2],
    [0, 2, 3],
    [5, 4, 7],
    [5, 7, 6],
    [8, 9, 10],
    [8, 10, 11],
    [14, 13, 12],
    [14, 12, 15],
    [16, 17, 18],
    [16, 18, 19],
    [23, 20, 21],
    [23, 21, 22],
]

BOTTOM = [
    [0.0, 1 / 3],
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1 / 3],
]

SIDE = [
    [0.0, 1 / 3],
    [0.0, 2 / 3],
    [1.0, 2 / 3],
    [1.0, 1 / 3],
]


TOP = [
    [0.0, 1.0],
    [0.0, 2 / 3],
    [1.0, 2 / 3],
    [1.0, 1.0],
]

UVS = [
    *TOP,
    *BOTTOM,
    *SIDE,
    *SIDE,
    *SIDE,
    *SIDE,
]

NOISE_FACTOR = 10.0
NOISE_AMPLITUDE = 25.0
NOISE_OCTAVES = 4
NOISE_PERSISTENCE = 0.3
NOISE_EXPONENT = 0.9

TEXTURE_WIDTH = 16
TEXTURE_HEIGHT = 48

TREE_CHANCE = 0.005
TREE_HEIGHT_RANGE = (5, 6)
DIRT_HEIGHT_RANGE = (3, 4)
WATER_LEVEL = 1

BLOCK_TYPES = {
    "air": 0,
    "stone": 1,
    "grass": 2,
    "dirt": 3,
    "oak_log": 4,
    "oak_leaves": 5,
    "water": 6,
}
