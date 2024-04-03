import numpy

from math.Math import Math
from world.chunk import Chunk


class World:
    def __init__(self):
        self.chunks = []

    def create_world(self):
        for x in range(1):
            for y in range(1):
                for z in range(1):
                    self.add_chunk(Math.Vector3(x, y, z))

    def add_chunk(self, position):
        chunk = Chunk(position)
        chunk.create_chunk()

        self.chunks.append(chunk)

    def render(self):
        for chunk in self.chunks:
            chunk.render()
