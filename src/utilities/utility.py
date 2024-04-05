import os

from pathlib import Path

from src.constants.file_constants import PATHS


class Utility:
    @staticmethod
    def get_root_path():
        return Path(__file__).parent.parent.parent

    @staticmethod
    def get_directory_path(paths):
        return os.path.join(Utility.get_root_path(), *paths)
