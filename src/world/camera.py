import math
import glm
import glfw

from src.math.math import Math

from src.constants.camera_constants import (
    CAMERA_PITCH,
    CAMERA_PITCH_LIMIT,
    CAMERA_SPEED,
    CAMERA_FOV,
    CAMERA_NEAR_CLIP,
    CAMERA_FAR_CLIP,
    CAMERA_DIRECTIONS,
    CAMERA_YAW,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Camera:
    def __init__(self):
        self.position = glm.vec3(0.0)

        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.mat4(1.0)

        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.yaw = CAMERA_YAW
        self.pitch = CAMERA_PITCH

        self.previous_time = 0
        self.speed = 0
        self.aspect_ratio = 0
        self.velocity = glm.vec3(0.0)

        self.previous_mouse_position = glm.vec2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def set_speed(self, time):
        delta_time = time - self.previous_time
        self.previous_time = time

        if glm.length(self.velocity) != 0.0:
            self.position += glm.normalize(self.velocity) * CAMERA_SPEED * delta_time
            self.velocity = glm.vec3(0.0)

    def set_movement(self, window, time):

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

        self.set_speed(time)

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

        if move_id in {"L", "R"}:
            self.velocity += direction * glm.normalize(glm.cross(self.front, self.up))

        if move_id in {"F", "B"}:
            self.velocity += direction * self.front

        if move_id in {"U", "D"}:
            self.velocity += direction * self.up

    def rotate(self, offset_mouse_x, offset_mouse_y):
        self.yaw += offset_mouse_x
        self.pitch = Math.clamp(self.pitch + offset_mouse_y, -CAMERA_PITCH_LIMIT, CAMERA_PITCH_LIMIT)

        camera_direction = glm.vec3(0.0)

        theta = glm.radians(self.yaw)
        omega = glm.radians(self.pitch)

        camera_direction.x = math.cos(theta) * math.cos(omega)
        camera_direction.y = math.sin(omega)
        camera_direction.z = math.sin(theta) * math.cos(omega)

        self.front = glm.normalize(camera_direction)
