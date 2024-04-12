import random
import numpy
import glm
import OpenGL.GL as gl

from src.buffer.buffer import Buffer
from src.buffer.texture import Texture

import src.utilities.noise as noise

from src.constants.world_constants import (
    BLOCK_TYPES,
    CHUNK_SIZE,
    UVS,
    VERTICES,
    INDICES,
    TREE_CHANCE,
    TREE_HEIGHT_RANGE,
    DIRT_HEIGHT_RANGE,
)


class Chunk:
    def __init__(self, world, x, y, z):
        self.opaque_vao = gl.glGenVertexArrays(1)
        self.transparent_vao = gl.glGenVertexArrays(1)

        self.world = world

        self.x = x
        self.y = y
        self.z = z

        self.blocks = {}
        self.block_data = {
            "opaque": {},
            "transparent": {},
        }

        Texture.use_textures()

    def create_chunk(self):
        for x in range(self.x, self.x + CHUNK_SIZE):
            for z in range(self.z, self.z + CHUNK_SIZE):
                y = noise.simplex_noise_2d(x, z)

                self.add_block(x, y, z)
                self.add_tree(x, y, z)
                self.add_cave(x, y, z)

    def add_tree(self, x, y, z):
        # if not check_tree_position_valid():
        #     return
        if random.random() > TREE_CHANCE:
            return

        tree_height = random.randint(*TREE_HEIGHT_RANGE)

        for dy in range(1, tree_height + 1):
            self.add_block(x, y + dy, z, "oak_log")

        self.add_leaves(x, y + tree_height - 2, z)

    def add_leaves(self, x, y, z):
        for dy in range(1, 3):
            for dx in range(-2, 3):
                for dz in range(-1, 2):
                    if dx == dz == 0:
                        continue

                    self.add_block(x + dx, y + dy, z + dz, "oak_leaves", "transparent")
                    self.add_block(x + dz, y + dy, z + dx, "oak_leaves", "transparent")

        for dy in range(3, 5):
            for dx, dz in ((-1, 0), (1, 0), (0, 0), (0, 1), (0, -1)):
                self.add_block(x + dx, y + dy, z + dz, "oak_leaves", "transparent")

    def add_cave(self, x, y, z):
        dirt_height = random.randint(*DIRT_HEIGHT_RANGE)

        for dy in range(1, dirt_height + 1):
            self.add_block(x, y - dy, z, "dirt")

        for dy in range(dirt_height, dirt_height + 10):
            if noise.simplex_noise_3d(x, y - dy, z) >= 0.0:
                self.add_block(x, y - dy, z, "stone")

    def add_block(self, x, y, z, block_type="grass", alpha_id="opaque"):
        position = (x, y, z)

        if not self.check_block_position_occupied(position):
            self.blocks[position] = BLOCK_TYPES[block_type]

        self.block_data[alpha_id][position] = BLOCK_TYPES[block_type]

    def check_block_position_occupied(self, position):
        for chunk in self.world.chunks.values():
            if position in chunk.blocks:
                return True

        return False

    def get_positions(self, alpha_id):
        return numpy.array(list(self.block_data[alpha_id].keys()), dtype=numpy.float32)

    def get_textures(self, alpha_id):
        return numpy.array(list(self.block_data[alpha_id].values()), dtype=numpy.float32)

    def set_buffers(self):
        gl.glBindVertexArray(self.opaque_vao)

        vertices = numpy.array(VERTICES, dtype=numpy.float32)
        indices = numpy.array(INDICES, dtype=numpy.uint8)
        uvs = numpy.array(UVS, dtype=numpy.float32)
        textures = self.get_textures("opaque")
        positions = self.get_positions("opaque")

        Buffer.use_buffer(vertices, gl.GL_ARRAY_BUFFER, location=0)
        Buffer.use_buffer(uvs, gl.GL_ARRAY_BUFFER, location=1)
        Buffer.use_buffer(indices, gl.GL_ELEMENT_ARRAY_BUFFER)
        Buffer.use_buffer(textures, gl.GL_ARRAY_BUFFER, location=2, instancing=True)
        Buffer.use_buffer(positions, gl.GL_ARRAY_BUFFER, location=4, instancing=True)

    def set_transparent_positions(self, camera_position):
        gl.glBindVertexArray(self.transparent_vao)

        data = [(glm.vec3(key), value) for key, value in self.block_data["transparent"].items()]
        data.sort(key=lambda x: glm.length2(camera_position - x[0]), reverse=True)

        positions = numpy.array([value[0] for value in data], dtype=numpy.float32)
        textures = numpy.array([value[1] for value in data], dtype=numpy.float32)

        # print(positions)

        vertices = numpy.array(VERTICES, dtype=numpy.float32)
        indices = numpy.array(INDICES, dtype=numpy.uint8)
        uvs = numpy.array(UVS, dtype=numpy.float32)

        Buffer.use_buffer(vertices, gl.GL_ARRAY_BUFFER, location=0)
        Buffer.use_buffer(uvs, gl.GL_ARRAY_BUFFER, location=1)
        Buffer.use_buffer(indices, gl.GL_ELEMENT_ARRAY_BUFFER)

        Buffer.use_buffer(textures, gl.GL_ARRAY_BUFFER, location=3, instancing=True)
        Buffer.use_buffer(positions, gl.GL_ARRAY_BUFFER, location=5, instancing=True)

    def render(self, camera_position, shader_manager, alpha_id):
        # self.set_buffers()
        is_transparent = alpha_id == "transparent"
        shader_manager.set_int1("mIsTransparent", int(is_transparent))

        if is_transparent:
            self.set_transparent_positions(camera_position)

        vao = self.transparent_vao if is_transparent else self.opaque_vao
        size = len(self.block_data[alpha_id])

        gl.glBindVertexArray(vao)
        gl.glDrawElementsInstanced(gl.GL_TRIANGLES, 36, gl.GL_UNSIGNED_BYTE, None, size)
        gl.glBindVertexArray(0)
