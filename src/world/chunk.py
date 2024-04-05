from collections import defaultdict

import numpy
import OpenGL.GL as gl


from src.constants.world_constants import CHUNK_SIZE, VERTICES, INDICES


class Chunk:
    def __init__(self, x, y, z):
        self.vao = None
        self.positions = []

        self.x = x
        self.y = y
        self.z = z

        self.blocks = {}

    def create_chunk(self):
        for x in range(self.x, self.x + CHUNK_SIZE):
            for y in range(self.y, self.y + CHUNK_SIZE):
                for z in range(self.z, self.z + CHUNK_SIZE):
                    self.add_block(x, y, z)

    def add_block(self, x, y, z, block_type=0):
        key = (x, y, z)

        if key not in self.blocks:
            self.blocks[key] = block_type

    def get_block_positions(self):
        return numpy.array(list(self.blocks.keys()), dtype=numpy.float32)

    def set_buffers(self):
        block_positions = self.get_block_positions()

        vertices = numpy.array(VERTICES, dtype=numpy.float32)
        indices = numpy.array(INDICES, dtype=numpy.uint32)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vbo = gl.glGenBuffers(1)

        # Bind buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices, gl.GL_STATIC_DRAW)
        # Send buffer data to GPU
        gl.glVertexAttribPointer(0, vertices.shape[1], gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(0)

        ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices, gl.GL_STATIC_DRAW)

        # uv at position 1, texture buffer at position 2, instancing at position 3
        ibo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, ibo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, block_positions, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(3, block_positions.shape[1], gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(3)
        gl.glVertexAttribDivisor(3, 1)

    def render(self):
        gl.glBindVertexArray(self.vao)
        gl.glDrawElementsInstanced(gl.GL_TRIANGLES, 36, gl.GL_UNSIGNED_INT, None, len(self.blocks.keys()))
        gl.glBindVertexArray(0)
