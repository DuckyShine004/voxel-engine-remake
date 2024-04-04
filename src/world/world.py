import numpy

from src.world.chunk import Chunk


class World:
    def __init__(self):
        self.chunks = numpy.empty(3 * [1], dtype=object)

    def create_world(self):
        for x in range(1):
            for y in range(1):
                for z in range(1):
                    self.add_chunk(x, y, z)

    def add_chunk(self, x, y, z):
        chunk = Chunk(x, y, z)
        chunk.create_chunk()

        self.chunks[x, y, z] = chunk

    def render(self):
        for x in range(1):
            for y in range(1):
                for z in range(1):
                    self.chunks[x, y, z].render()