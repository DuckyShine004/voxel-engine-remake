import os
import glm

import OpenGL.GL as gl

from src.utilities.utility import Utility
from src.constants.file_constants import PATHS


class ShaderManager:
    def __init__(self):
        self.vert_shader = None
        self.frag_shader = None

        self.vert_shader_source = None
        self.frag_shader_source = None

        self.program_id = None

        self.create_program()

    def create_program(self):
        self.set_shaders()
        self.compile_shaders()
        self.attach_shaders()

    def validate_compile_status(self, shader):
        status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)

        if not status:
            error_log = gl.glGetShaderInfoLog(shader).decode()
            raise RuntimeError(f"Shader Compilation Failed:\n{error_log}")

    def validate_linking_status(self):
        status = gl.glGetProgramiv(self.program_id, gl.GL_LINK_STATUS)

        if not status:
            error_log = gl.glGetShaderInfoLog(self.program_id).decode()
            raise RuntimeError(f"Program Linking Failed:\n{error_log}")

    def set_shaders(self):
        shader_path = Utility.get_directory_path(PATHS["shaders"])

        self.vert_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        vert_shader_path = os.path.join(shader_path, "vert.glsl")
        frag_shader_path = os.path.join(shader_path, "frag.glsl")

        with open(vert_shader_path, "r", encoding="utf-8") as vert_shader_file:
            self.vert_shader_source = vert_shader_file.read()

        with open(frag_shader_path, "r", encoding="utf-8") as frag_shader_file:
            self.frag_shader_source = frag_shader_file.read()

    def compile_shaders(self):
        gl.glShaderSource(self.vert_shader, self.vert_shader_source)
        gl.glShaderSource(self.frag_shader, self.frag_shader_source)

        gl.glCompileShader(self.vert_shader)
        self.validate_compile_status(self.vert_shader)

        gl.glCompileShader(self.frag_shader)
        self.validate_compile_status(self.frag_shader)

    def attach_shaders(self):
        self.program_id = gl.glCreateProgram()

        gl.glAttachShader(self.program_id, self.vert_shader)
        gl.glAttachShader(self.program_id, self.frag_shader)

        gl.glLinkProgram(self.program_id)
        self.validate_linking_status()

        gl.glDeleteShader(self.vert_shader)
        gl.glDeleteShader(self.frag_shader)

    def use_program(self):
        gl.glUseProgram(self.program_id)

    def set_int1(self, name, value):
        location = gl.glGetUniformLocation(self.program_id, name)
        gl.glUniform1i(location, value)

    def set_vec3(self, name, value):
        location = gl.glGetUniformLocation(self.program_id, name)
        gl.glUniform3fv(location, 1, glm.value_ptr(value))

    def set_mat4(self, name, value):
        location = gl.glGetUniformLocation(self.program_id, name)
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(value))
