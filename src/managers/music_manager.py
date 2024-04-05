import os
import pygame

from src.utilities.utility import Utility
from src.constants.file_constants import PATHS


class MusicManager:
    def __init__(self):
        self.playlist = self.get_playlist()

    def get_playlist(self):
        music_path = Utility.get_directory_path(PATHS["music"])

        print(music_path, os.listdir(music_path))

        return 1

    def update(self):
        pass
