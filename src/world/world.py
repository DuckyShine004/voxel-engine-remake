import numpy
import OpenGL.GL as gl

from src.world.chunk import Chunk

from src.constants.world_constants import CHUNK_SIZE, WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH


class World:
    def __init__(self):
        self.chunks = {}

    def create_world(self):
        for x in range(WORLD_WIDTH):
            # for y in range(WORLD_HEIGHT):
            for z in range(WORLD_DEPTH):
                self.add_chunk(x, 0, z)

    def add_chunk(self, x, y, z):
        chunk = Chunk(self, x * CHUNK_SIZE, y * CHUNK_SIZE, z * CHUNK_SIZE)
        position = (x, y, z)

        chunk.create_chunk()
        chunk.set_buffers()

        if position not in self.chunks:
            self.chunks[position] = chunk

    def render(self, camera_position, shader_manager):
        for chunk in self.chunks.values():
            chunk.render(camera_position, shader_manager, "opaque")

        for chunk in self.chunks.values():
            chunk.render(camera_position, shader_manager, "transparent")
