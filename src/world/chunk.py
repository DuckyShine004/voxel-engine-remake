import numpy
import OpenGL.GL as gl

from src.buffer.buffer import Buffer
from src.managers.texture_manager import TextureManager
import src.utilities.noise as noise

from src.constants.world_constants import CHUNK_SIZE, UVS, VERTICES, INDICES


class Chunk:
    def __init__(self, x, y, z):
        self.vao = None
        self.tao = None

        self.x = x
        self.y = y
        self.z = z

        self.blocks = {}

    def create_chunk(self):
        for x in range(self.x, self.x + CHUNK_SIZE):
            for z in range(self.z, self.z + CHUNK_SIZE):
                y = noise.simplex_noise_2d(x, z)
                # print(y)

                self.add_block(x, y, z)

    def add_block(self, x, y, z, block_type=2):
        position = (x, y, z)

        if position not in self.blocks:
            self.blocks[position] = block_type

    def get_block_positions(self):
        return numpy.array(list(self.blocks.keys()), dtype=numpy.float32)

    def get_block_textures(self):
        return numpy.array(list(self.blocks.values()), dtype=numpy.float32)

    def set_buffers(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        self.tao = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.tao)
        TextureManager()

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        block_textures = self.get_block_textures()
        block_positions = self.get_block_positions()

        vertices = numpy.array(VERTICES, dtype=numpy.float32)
        indices = numpy.array(INDICES, dtype=numpy.uint8)
        uvs = numpy.array(UVS, dtype=numpy.float32)

        Buffer.use_buffer(vertices, gl.GL_ARRAY_BUFFER, location=0)
        Buffer.use_buffer(uvs, gl.GL_ARRAY_BUFFER, location=1)
        Buffer.use_buffer(indices, gl.GL_ELEMENT_ARRAY_BUFFER)
        Buffer.use_buffer(block_textures, gl.GL_ARRAY_BUFFER, location=2, instancing=True)
        Buffer.use_buffer(block_positions, gl.GL_ARRAY_BUFFER, location=3, instancing=True)

    def render(self):
        gl.glBindVertexArray(self.vao)
        gl.glDrawElementsInstanced(gl.GL_TRIANGLES, 36, gl.GL_UNSIGNED_BYTE, None, len(self.blocks.keys()))
        gl.glBindVertexArray(0)
