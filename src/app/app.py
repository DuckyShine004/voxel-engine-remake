import glfw
import OpenGL.GL as gl

from src.managers.shader_manager import ShaderManager
from src.world.world import World
from src.world.camera import Camera

from src.constants.camera_constants import CAMERA_SENSITIVITY


class App:
    def __init__(self, window):
        self.window = window

        self.world = World()
        self.camera = Camera()
        self.shader_manager = ShaderManager()

    def initialize_application_parameters(self):
        self.world.create_world()

        glfw.set_framebuffer_size_callback(self.window, self.on_resize)
        glfw.set_key_callback(self.window, self.on_key_press)
        glfw.set_cursor_pos_callback(self.window, self.on_mouse)

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
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
        self.camera.update(self.window, self.shader_manager, time)

    def render(self):
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.world.render()

    def on_key_press(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def on_resize(self, window, width, height):
        gl.glViewport(0, 0, width, height)

        self.camera.set_aspect_ratio(width, height)

    def on_mouse(self, window, mouse_x, mouse_y):
        offset_mouse_x = (mouse_x - self.camera.previous_mouse_position.x) * CAMERA_SENSITIVITY
        offset_mouse_y = (self.camera.previous_mouse_position.y - mouse_y) * CAMERA_SENSITIVITY

        self.camera.previous_mouse_position.x = mouse_x
        self.camera.previous_mouse_position.y = mouse_y

        self.camera.rotate(offset_mouse_x, offset_mouse_y)
