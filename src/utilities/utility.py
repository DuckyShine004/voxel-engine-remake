import os

from pathlib import Path


class Utility:
    @staticmethod
    def get_root_path():
        return Path(__file__).parent.parent.parent

    @staticmethod
    def get_shader_path():
        return os.path.join(Utility.get_root_path(), "shaders")
