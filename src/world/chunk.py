import numpy
import OpenGL.GL as gl

from src.constants.world_constants import VERTICES, INDICES


class Chunk:
    def __init__(self, x, y, z):
        self.vao = None
        self.positions = []

        self.x = x
        self.y = y
        self.z = z

        self.blocks = numpy.zeros(3 * [1], dtype=numpy.uint8)
        self.block_positions = self.get_block_positions()
        self.set_buffers(self.block_positions)

    def create_chunk(self):
        for x in range(1):
            for y in range(1):
                for z in range(1):
                    self.add_block(x, y, z)

    def add_block(self, x, y, z, block_type=0):
        self.blocks[x, y, z] = block_type

    def get_block_positions(self):
        block_positions = []

        for x in range(1):
            for y in range(1):
                for z in range(1):
                    block_positions.append((x, y, z))

        return numpy.array(block_positions, dtype=numpy.float32)

    def set_buffers(self, block_positions):
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
        gl.glDrawElementsInstanced(gl.GL_TRIANGLES, 36, gl.GL_UNSIGNED_INT, None, len(self.block_positions))
        gl.glBindVertexArray(0)
