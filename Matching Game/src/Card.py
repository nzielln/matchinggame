class Card:
    instances = []

    def __init__(self, name, image, x, y, back_stamp, card_stamp=None, clicked=False):
        self.name = name
        self.image = image
        self.x = x
        self.y = y
        self.clicked = False
        self.back_stamp = back_stamp
        self.card_stamp = None
        self.__class__.instances.append(self)

    def __eq__(self, other):
        if self.image[:-4] == other.image[:-10] or self.image[:-10] == other.image[:-4]:
            return True
        else:
            return False
