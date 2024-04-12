class Math:
    @staticmethod
    def clamp(value, lower, upper):
        if value < lower:
            return lower

        if value > upper:
            return upper

        return value

    @staticmethod
    def length2(position):
        return pow(position.x, 2) + pow(position.y, 2) + pow(position.z, 2)
