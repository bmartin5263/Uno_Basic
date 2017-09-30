from card import Card
import random

class Deck():
    ''''shuffle' (bool) : shuffle deck.'''

    colors = ('red', 'yellow', 'green', 'blue')
    values = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'R', '+2')

    def __init__(self, populate):
        '''Initializes proper deck of 108 Uno Cards.'''
        self.deck = []
        if populate:
            self.populate(True)

    def __getitem__(self, index):
        return self.deck[index]

    def populate(self, shuffle=True):
        for color in self.colors:
            for value in self.values:
                self.deck.append(Card(color, value))
                if value != '0':
                    self.deck.append(Card(color, value))
        for i in range(4):
            i  # unused
            self.deck.append(Card('wild', '+4'))
            self.deck.append(Card('wild', 'W'))
        if shuffle:
            self.shuffle()

    def __iter__(self):
        return iter(self.deck)

    def __len__(self):
        return len(self.deck)

    def draw(self):
        return self.deck.pop()

    def insert(self, card):
        self.deck.insert(0, card)

    def shuffle(self):
        random.shuffle(self.deck)