import os
import OpenGL.GL as gl

from PIL import Image
from numba.core.ir_utils import numpy

from src.utilities.utility import Utility

from src.constants.file_constants import PATHS
from src.constants.world_constants import TEXTURE_WIDTH, TEXTURE_HEIGHT, BLOCK_TYPES


class TextureManager:
    def __init__(self):
        self.initialize_texture_parameters()
        self.create_texture_atlases()

    def initialize_texture_parameters(self):
        gl.glTexImage3D(
            gl.GL_TEXTURE_2D_ARRAY,
            0,
            gl.GL_RGBA,
            TEXTURE_WIDTH,
            TEXTURE_HEIGHT,
            len(BLOCK_TYPES) - 1,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            None,
        )

    def create_texture_atlas(self, block_path, block_index):
        block_files = os.listdir(block_path)
        block_atlas = None

        for block_file in block_files:
            block_image = Image.open(os.path.join(block_path, block_file))
            block_image_data = numpy.array(block_image.convert("RGBA"), dtype=numpy.uint8)

            if block_atlas is None:
                block_atlas = block_image_data
                continue

            block_atlas = numpy.concatenate([block_atlas, block_image_data], axis=0)

    def create_texture_atlases(self):
        block_data = self.get_block_data()

        for block_path, block_index in block_data:
            self.create_texture_atlas(block_path, block_index)

    def get_block_data(self):
        texture_path = Utility.get_directory_path(PATHS["block_textures"])
        block_data = []

        for block_type, block_index in BLOCK_TYPES.items():
            block_data.append((os.path.join(texture_path, block_type), block_index))

        return block_data
