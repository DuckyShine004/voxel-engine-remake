import numpy

from src.world.chunk import Chunk

from src.constants.world_constants import CHUNK_SIZE, WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH


class World:
    def __init__(self):
        self.chunks = numpy.empty((WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH), dtype=object)

    def create_world(self):
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                for z in range(WORLD_DEPTH):
                    self.add_chunk(x, y, z)

    def add_chunk(self, x, y, z):
        chunk = Chunk(x * CHUNK_SIZE, y * CHUNK_SIZE, z * CHUNK_SIZE)

        chunk.create_chunk()
        chunk.set_buffers()

        self.chunks[x, y, z] = chunk

    def render(self):
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                for z in range(WORLD_DEPTH):
                    self.chunks[x, y, z].render()
