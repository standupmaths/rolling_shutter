class Vec2(list):
    def __init__(self, x, y=None):
        super().__init__(self)
        self.append(x)
        if y is None:
            y = x
        self.append(y)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, x):
        self[0] = x

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, y):
        self[1] = y

    def __add__(self, other):
        if isinstance(other, list):
            return Vec2(self.x + other[0], self.y + other[1])
        else:
            return Vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, list):
            return Vec2(self.x - other[0], self.y - other[1])
        else:
            return Vec2(self.x - other, self.y - other)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __floordiv__(self, other):
        return Vec2(self.x // other, self.y // other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __inv__(self, other):
        return Vec2(-self.x, -self.y)
