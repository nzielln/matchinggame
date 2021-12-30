class GameData:
    obj = []

    def __init__(self, name, leaders, matches, guesses, clicked_cards):
        self.leaders = leaders
        self.guesses = guesses
        self.matches = matches
        self.name = name
        self.clicked_cards = []
        self.__class__.obj.append(self)
