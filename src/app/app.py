import glfw
import OpenGL.GL as gl

from src.managers.shader_manager import ShaderManager
from src.world.world import World


class App:
    def __init__(self, window):
        self.window = window

        self.world = World()
        self.shader_manager = ShaderManager()

    def initialize_application_parameters(self):
        self.world.create_world()

        glfw.set_framebuffer_size_callback(self.window, self.on_resize)
        glfw.set_key_callback(self.window, self.on_key_press)

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.shader_manager.use_program()

    def run(self):
        self.initialize_application_parameters()

        while not glfw.window_should_close(self.window):
            self.update()
            self.render()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.destroy_window(self.window)
        glfw.terminate()

    def update(self):
        time = glfw.get_time()
        self.world.update(self.shader_manager, time)

    def render(self):
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.world.render()

    def on_key_press(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def on_resize(self, window, width, height):
        gl.glViewport(0, 0, width, height)

        self.world.camera.set_aspect_ratio(width, height)
