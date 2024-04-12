import glm
import numpy
import random

import OpenGL.GL as gl

from src.math.math import Math

from src.buffer.buffer import Buffer
from src.buffer.texture import Texture

from src.utilities import noise

from src.constants.world_constants import (
    BLOCK_TYPES,
    CHUNK_SIZE,
    DIRT_HEIGHT_RANGE,
    TREE_CHANCE,
    TREE_HEIGHT_RANGE,
    VERTICES,
    INDICES,
    UVS,
    WORLD_WIDTH,
    WORLD_DEPTH,
)


class World:
    def __init__(self):
        self.chunks = {}

        self.model_data = {
            "vertices": None,
            "indices": None,
            "uvs": None,
        }

        self.vertex_arrays = {
            "opaque": None,
            "transparent": None,
        }

        self.buffers = {
            "vertex": None,
            "index": None,
            "element": None,
            "uv": None,
            "opaque_texture": None,
            "transparent_texture": None,
            "opaque_instance": None,
            "transparent_instance": None,
        }

        self.block_data = {
            "all": {},
            "opaque": {},
            "transparent": {},
        }

        self.set_parameters()

    def set_parameters(self):
        Texture.use_textures()

        self.model_data["uvs"] = numpy.array(UVS, dtype=numpy.float32)
        self.model_data["indices"] = numpy.array(INDICES, dtype=numpy.uint8)
        self.model_data["vertices"] = numpy.array(VERTICES, dtype=numpy.float32)

        for key in self.vertex_arrays:
            self.vertex_arrays[key] = gl.glGenVertexArrays(1)

        for key in self.buffers:
            self.buffers[key] = gl.glGenBuffers(1)

    def set_opaque_buffers(self):
        gl.glBindVertexArray(self.vertex_arrays["opaque"])

        positions = self.get_positions("opaque")
        textures = self.get_textures("opaque")

        Buffer.use_buffer(self.buffers["vertex"], self.model_data["vertices"], gl.GL_ARRAY_BUFFER, location=0)
        Buffer.use_buffer(self.buffers["uv"], self.model_data["uvs"], gl.GL_ARRAY_BUFFER, location=1)
        Buffer.use_buffer(self.buffers["index"], self.model_data["indices"], gl.GL_ELEMENT_ARRAY_BUFFER)
        Buffer.use_buffer(self.buffers["opaque_texture"], textures, gl.GL_ARRAY_BUFFER, location=2, instancing=True)
        Buffer.use_buffer(self.buffers["opaque_instance"], positions, gl.GL_ARRAY_BUFFER, location=4, instancing=True)

    def set_transparent_buffers(self, camera_position):
        gl.glBindVertexArray(self.vertex_arrays["transparent"])

        sorted_block_data = self.get_sorted_block_data(camera_position, "transparent")
        positions = []
        textures = []

        for position, texture in sorted_block_data:
            positions.append(position)
            textures.append(texture)

        positions = numpy.array(positions, dtype=numpy.float32)
        textures = numpy.array(textures, dtype=numpy.float32)

        Buffer.use_buffer(self.buffers["vertex"], self.model_data["vertices"], gl.GL_ARRAY_BUFFER, location=0)
        Buffer.use_buffer(self.buffers["uv"], self.model_data["uvs"], gl.GL_ARRAY_BUFFER, location=1)
        Buffer.use_buffer(self.buffers["index"], self.model_data["indices"], gl.GL_ELEMENT_ARRAY_BUFFER)
        Buffer.use_buffer(self.buffers["transparent_texture"], textures, gl.GL_ARRAY_BUFFER, location=3, instancing=True)
        Buffer.use_buffer(self.buffers["transparent_instance"], positions, gl.GL_ARRAY_BUFFER, location=5, instancing=True)

    def get_sorted_block_data(self, camera_position, alpha_type):
        return sorted(self.block_data[alpha_type].items(), key=lambda x: -Math.length2(camera_position - x[0]))

    def get_positions(self, alpha_type):
        return numpy.array(list(self.block_data[alpha_type].keys()), dtype=numpy.float32)

    def get_textures(self, alpha_type):
        return numpy.array(list(self.block_data[alpha_type].values()), dtype=numpy.float32)

    def create_world(self):
        for x in range(WORLD_WIDTH):
            for z in range(WORLD_DEPTH):
                self.create_chunk(x * CHUNK_SIZE, z * CHUNK_SIZE)

        self.set_opaque_buffers()

    def create_chunk(self, dx, dz):
        for x in range(dx, dx + CHUNK_SIZE):
            for z in range(dz, dz + CHUNK_SIZE):
                y = noise.simplex_noise_2d(x, z)

                self.add_block(x, y, z)
                self.add_tree(x, y, z)
                self.add_cave(x, y, z)

    def add_block(self, x, y, z, block_type="grass", alpha_type="opaque"):
        position = (x, y, z)

        if position not in self.block_data["all"]:
            self.block_data[alpha_type][position] = BLOCK_TYPES[block_type]
            self.block_data["all"][position] = self.block_data[alpha_type][position]

    def add_tree(self, x, y, z):
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

    def render(self, camera_position, shader_manager, alpha_type):
        is_transparent = alpha_type == "transparent"
        shader_manager.set_int1("mIsTransparent", int(is_transparent))

        if is_transparent:
            self.set_transparent_buffers(camera_position)

        vertex_array = self.vertex_arrays["transparent"] if is_transparent else self.vertex_arrays["opaque"]
        size_of_data = len(self.block_data[alpha_type])

        gl.glBindVertexArray(vertex_array)
        gl.glDrawElementsInstanced(gl.GL_TRIANGLES, 36, gl.GL_UNSIGNED_BYTE, None, size_of_data)
        gl.glBindVertexArray(0)
