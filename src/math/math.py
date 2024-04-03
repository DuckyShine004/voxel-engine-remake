import pyrr
import numpy


class Math:
    @staticmethod
    def Vector3(x, y, z):
        return pyrr.Vector3([x, y, z], dtype=numpy.float32)
