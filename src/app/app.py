import glfw

from src.managers.shader_manager import ShaderManager


class App:
    def __init__(self, window):
        self.window = window
        self.shader_manager = ShaderManager()

    def run(self):
        while not glfw.window_should_close(self.window):

            glfw.swap_buffers(self.window)

            glfw.poll_events()
