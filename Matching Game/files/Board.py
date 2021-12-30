class Board:
    instances = []

    def __init__(self, name, tur, x, y, stamp=None):
        self.name = name
        self.tur = tur
        self.x = x
        self.y = y
        self.stamp = stamp
        self.__class__.instances.append(self)
