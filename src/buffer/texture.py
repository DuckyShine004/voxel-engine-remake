import os
import OpenGL.GL as gl

from PIL import Image
from numba.core.ir_utils import numpy

from src.utilities.utility import Utility

from src.constants.file_constants import PATHS
from src.constants.world_constants import TEXTURE_WIDTH, TEXTURE_HEIGHT, BLOCK_TYPES


class Texture:
    @staticmethod
    def use_textures():
        texture_object = gl.glGenTextures(1)

        Texture.initialize_texture_parameters(texture_object)
        Texture.create_texture_atlases()

    @staticmethod
    def initialize_texture_parameters(texture_object):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, texture_object)

        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

        gl.glTexImage3D(
            gl.GL_TEXTURE_2D_ARRAY,
            0,
            gl.GL_RGBA,
            TEXTURE_WIDTH,
            TEXTURE_HEIGHT,
            len(BLOCK_TYPES),
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            None,
        )

    @staticmethod
    def create_texture_atlas(block_path, block_index):
        block_files = sorted(os.listdir(block_path))
        block_atlas = None

        for block_file in block_files:
            block_image = Image.open(os.path.join(block_path, block_file))
            block_image_data = numpy.array(block_image.convert("RGBA"), dtype=numpy.uint8)

            if block_atlas is None:
                block_atlas = block_image_data
                continue

            block_atlas = numpy.concatenate([block_atlas, block_image_data], axis=0)

        Texture.add_texture_atlas(block_atlas, block_index)

    @staticmethod
    def add_texture_atlas(texture_atlas, texture_atlas_index):
        gl.glTexSubImage3D(
            gl.GL_TEXTURE_2D_ARRAY,
            0,
            0,
            0,
            texture_atlas_index,
            TEXTURE_WIDTH,
            TEXTURE_HEIGHT,
            1,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            texture_atlas,
        )

    @staticmethod
    def create_texture_atlases():
        block_data = Texture.get_block_data()

        for block_path, block_index in block_data:
            Texture.create_texture_atlas(block_path, block_index)

    @staticmethod
    def get_block_data():
        texture_path = Utility.get_directory_path(PATHS["textures"])
        block_data = []

        for block_type, block_index in BLOCK_TYPES.items():
            if block_type == "air":
                continue

            block_directory = ["blocks", block_type]
            block_data.append((os.path.join(texture_path, *block_directory), block_index))

        return block_data
