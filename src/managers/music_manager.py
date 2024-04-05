import os
import pygame
import random

from src.utilities.utility import Utility
from src.constants.file_constants import PATHS


class MusicManager:
    def __init__(self):
        self.playlist = self.get_playlist()

    def get_playlist(self):
        music_path = Utility.get_directory_path(PATHS["music"])
        playlist = []

        for file in os.listdir(music_path):
            if not file.startswith("."):
                playlist.append(os.path.join(music_path, file))

        return playlist

    def play_music(self):
        music_file_path = random.choice(self.playlist)

        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.play()

        print(f"now playing {music_file_path}")

    def update(self):
        if not pygame.mixer.music.get_busy():
            self.play_music()
