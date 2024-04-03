import sys
import glfw

from src.app.app import App


def main():
    if not glfw.init():
        sys.exit(0)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

    window = glfw.create_window(1080, 720, "Voxel Engine", None, None)

    if not window:
        glfw.terminate()
        sys.exit(0)

    glfw.make_context_current(window)
    App(window).run()


if __name__ == "__main__":
    main()
