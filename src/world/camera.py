import glm
import glfw

from src.constants.camera_constants import (
    CAMERA_SPEED,
    CAMERA_FOV,
    CAMERA_NEAR_CLIP,
    CAMERA_FAR_CLIP,
    CAMERA_DIRECTIONS,
)


class Camera:
    def __init__(self):
        self.position = glm.vec3(0.0)

        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.mat4(1.0)

        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.previous_time = 0
        self.speed = 0
        self.aspect_ratio = 0

    def set_speed(self, time):
        delta_time = time - self.previous_time
        self.previous_time = time
        self.speed = CAMERA_SPEED * delta_time

    def set_movement(self, window, time):
        self.set_speed(time)
        print(self.position)

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.move("F")

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.move("B")

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.move("L")

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.move("R")

        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.move("U")

        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.move("D")

    def set_aspect_ratio(self, screen_width, screen_height):
        self.aspect_ratio = screen_width / screen_height

    def set_view_matrix(self):
        self.view_matrix = glm.lookAt(self.position, self.position + self.front, self.up)

    def set_projection_matrix(self):
        theta = glm.radians(CAMERA_FOV)
        camera_clip_range = (CAMERA_NEAR_CLIP, CAMERA_FAR_CLIP)
        self.projection_matrix = glm.perspective(theta, self.aspect_ratio, *camera_clip_range)

    def set_shader_attributes(self, shader_manager):
        projection_view_matrix = self.projection_matrix * self.view_matrix

        shader_manager.set_vec3("mCameraPos", self.position)
        shader_manager.set_mat4("mProjectionView", projection_view_matrix)

    def update(self, window, shader_manager, time):
        self.set_movement(window, time)
        self.set_view_matrix()
        self.set_projection_matrix()
        self.set_shader_attributes(shader_manager)

    def move(self, move_id):
        direction = CAMERA_DIRECTIONS[move_id]
        camera_velocity = direction * self.speed

        if move_id in {"L", "R"}:
            self.position += camera_velocity * glm.normalize(glm.cross(self.front, self.up))

        if move_id in {"F", "B"}:
            self.position += camera_velocity * self.front

        if move_id in {"U", "D"}:
            self.position += camera_velocity * self.up
