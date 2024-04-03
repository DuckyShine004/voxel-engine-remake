from src.math.math import Math

from src.constants.world_constants import CHUNK_SIZE


class Chunk:
    def __init__(self, position):
        self.position = position
        self.blocks = numpy.zeros(3 * [CHUNK_SIZE])

    def create_chunk(self):
        for x in range(1):
            for y in range(1):
                for z in range(1):
                    self.add_block(Math.Vector3(x, y, z))

    def add_block(self, position):
        self.blocks.append()

    def render(self): ...
