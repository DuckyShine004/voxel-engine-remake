import OpenGL.GL as gl


class Buffer:
    @staticmethod
    def use_buffer(buffer, data, target, location=None, instancing=False):
        buffer_offset = data.shape[1] if len(data.shape) > 1 else 1

        Buffer.bind_buffer_data(buffer, target, data)

        if location is not None:
            Buffer.send_buffer_data(buffer_offset, location, instancing)

    @staticmethod
    def bind_buffer_data(buffer, target, data):
        gl.glBindBuffer(target, buffer)
        gl.glBufferData(target, data, gl.GL_STATIC_DRAW)

    @staticmethod
    def send_buffer_data(buffer_offset, location, instancing):
        gl.glVertexAttribPointer(location, buffer_offset, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(location)

        if instancing:
            gl.glVertexAttribDivisor(location, 1)
