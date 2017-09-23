class Card():
    '''
    'suit' (string) : Card's Color (rgby)
    'rank' (string) : Card's Value (0-9, R, X, W, +2, +4)
    '''

    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'wild': '',
        'dwild': '',
        'dred': '\033[31m',
        'dgreen': '\033[32m',
        'dyellow': '\033[33m',
        'dblue': '\033[34m',
        'dpurple': '\033[35m',
        'dcyan': '\033[36m',
        'dwhite': '\033[37m',
    }

    idMap = {
        'red': 'R', 'blue': 'B', 'green': 'G', 'yellow': 'Y', 'wild': 'W',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        '+2': '+', 'R': 'R', 'W': 'W', '+4': '$', 'X': 'X'
    }

    bigNums = {
        "0": [" .d888b. ", "d88P Y88b", "888   888", "888   888", "888   888", "888   888", "d88P Y88b", " \"Y888P\" "],
        "1": ["  d888   ", " d8888   ", "   888   ", "   888   ", "   888   ", "   888   ", "   888   ", " 8888888 "],
        "2": [".d8888b. ", "d88P  Y88", "d8    888", "    .d88P", ".od888P\" ", "d88P\"    ", "888\"     ",
              "888888888"],
        "3": [" .d8888b.", "d88P  Y88", "     .d88", "   8888\" ", "     \"Y8b", "888    88", "Y88b  d88",
              " \"Y8888P\""],
        "4": ["    d88b ", "   d8P88 ", "  d8  88 ", " d8   88 ", "d8    88 ", "888888888", "      88 ", "      88 "],
        "5": ["888888888", "888      ", "888      ", "8888888b ", "   \"Y88b ", "      888", "Y88b d88P",
              "\"Y8888P\" "],
        "6": [" .d888b. ", "d88P Y88b", "888      ", "888d888b ", "888P \"Y8b", "888   888", "Y88b d88b",
              " \"Y888P\" "],
        "7": ["888888888", "      d8P", "     d8P ", "    d8P  ", " 8888888 ", "  d8P    ", " d8P     ", "d8P      "],
        "8": [" .d888b. ", "d8P   Y8b", "Y8b.  d8P", " \"Y8888\" ", " .dP\"Yb. ", "888   888", "Y88b d88P",
              " \"Y888P\" "],
        "9": [" .d888b. ", "d8P   Y8b", "88     88", "Y8b.  d88", " \"Y88P888", "      888", "Y88b d88P",
              " \"Y888P\" "],
        "X": ["Y8b   d8P", " Y8b d8P ", "  Y8o8P  ", "   Y8P   ", "   d8b   ", "  d888b  ", " d8P Y8b ", "d8P   Y8b"],
        "W": ["88     88", "88     88", "88  o  88", "88 d8b 88", "88d888b88", "88P   Y88", "8P     Y8", "P       Y"],
        "+2": ["  db     ", "  88     ", "C8888D   ", "  88 8888", "  VP    8", "     8888", "     8   ", "     8888"],
        "+4": ["  db     ", "  88     ", "C8888D   ", "  88   d ", "  VP  d8 ", "     d 8 ", "    d8888", "       8 "],
        "R9": ["    d88P ", "   d88P  ", "  d88P   ", " d88P    ", " Y88b    ", "  Y88b   ", "   Y88b  ", "    Y88b "],
        "R8": ["   d88P  ", "  d88P   ", " d88P    ", "d88P     ", "Y88b     ", " Y88b    ", "  Y88b   ", "   Y88b  "],
        "R7": ["  d88P  Y", " d88P    ", "d88P     ", "88P      ", "88b      ", "Y88b     ", " Y88b    ", "  Y88b  d"],
        "R6": [" d88P  Y8", "d88P    Y", "88P      ", "8P       ", "8b       ", "88b      ", "Y88b    d", " Y88b  d8"],
        "R5": ["d88P  Y88", "88P    Y8", "8P      Y", "P        ", "b        ", "8b      d", "88b    d8", "Y88b  d88"],
        "R4": ["88P  Y88b", "8P    Y88", "P      Y8", "        Y", "        d", "b      d8", "8b    d88", "88b  d88P"],
        "R3": ["8P  Y88b ", "P    Y88b", "      Y88", "       Y8", "       d8", "      d88", "b    d88P", "8b  d88P "],
        "R2": ["P  Y88b  ", "    Y88b ", "     Y88b", "      Y88", "      d88", "     d88P", "    d88P ", "b  d88P  "],
        "R1": ["  Y88b   ", "   Y88b  ", "    Y88b ", "     Y88b", "     d88P", "    d88P ", "   d88P  ", "  d88P   "],
        "R0": [" Y88b    ", "  Y88b   ", "   Y88b  ", "    Y88b ", "    d88P ", "   d88P  ", "  d88P   ", " d88P    "],
    }

    def __init__(self, color, value):
        '''Initializes Uno Card w/ Color and Value.'''
        self.wild = False  # Is wild card?
        self.zero = False
        self.cardID = '{}{}'.format(self.idMap[color], self.idMap[value])
        self.setColor(color)
        self.setValue(value)
        self.setPoints(value)

    #############################################

    ### -\/-  Retrieve Card Information  -\/- ###

    def __repr__(self):
        return "{},{}".format(self.color, self.value)

    def getBigNum(self, reverse, reverseSeed=0):
        '''Returns list of strings to draw card's value on the pile.'''
        bigNums = []
        colorCode = self.colorCode
        colorCodeDark = self.colorCodeDark
        value = self.value
        if value == 'R':
            if not reverse:
                value += str(reverseSeed)
            else:
                value += str(9 - reverseSeed)
        for mid in self.bigNums[value]:
            bigNums += ['{}| |{}'.format(colorCode, colorCodeDark) + mid + '{}| |\033[0m\t'.format(colorCode)]

        return bigNums

    def getColor(self):
        '''Returns card's color.'''
        return self.color

    def getColorCode(self):
        '''Returns card's color code.'''
        return self.colorCode

    def getValue(self):
        '''Returns card's value.'''
        return self.value

    def getPoints(self):
        '''Returns card's point value.'''
        return self.points

    def getRow(self, rowNum, hide=False):
        value = self.value
        displaySpace = self.displaySpace
        if hide:
            colorCode = '\033[97m'
            value = '?'
            displaySpace = ' '
        else:
            colorCode = self.colorCode
            if self.isWild():
                if rowNum == 0:
                    colorCode = '\033[91m'
                elif rowNum == 1:
                    colorCode = '\033[93m'
                elif rowNum == 2:
                    colorCode = '\033[92m'
                elif rowNum == 3:
                    colorCode = '\033[94m'

        if rowNum == 0:
            return '{}\u2666--\u2666\033[0m'.format(colorCode)
        elif rowNum == 1:
            return '{}|{}{}|\033[0m'.format(colorCode, displaySpace, value)
        elif rowNum == 2:
            if hide:
                return '{}|? |\033[0m'.format(colorCode)
            else:
                return '{}|  |\033[0m'.format(colorCode)
        elif rowNum == 3:
            return '{}\u2666--\u2666\033[0m'.format(colorCode)

    #############################################

    ### -\/-  Set Card Information  -\/- ###

    def setColor(self, color):
        '''Sets Card's color and escape code.'''
        if color == 'blue':
            self.color = 'blue'
            self.colorCode = self.colors['blue']
            self.colorCodeDark = self.colors['dblue']
        elif color == 'red':
            self.color = 'red'
            self.colorCode = self.colors['red']
            self.colorCodeDark = self.colors['dred']
        elif color == 'yellow':
            self.color = 'yellow'
            self.colorCode = self.colors['yellow']
            self.colorCodeDark = self.colors['dyellow']
        elif color == 'green':
            self.color = 'green'
            self.colorCode = self.colors['green']
            self.colorCodeDark = self.colors['dgreen']
        elif color == 'wild':  # No color modification
            self.wild = True
            self.color = 'wild'
            self.colorCodeDark = self.colors['dwild']
            self.colorCode = self.colors['wild']

    def setValue(self, value):
        if value in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'R', '+2', '+4', 'W'):
            self.value = value
            self.displaySpace = ' '
            if len(value) == 2:
                self.displaySpace = ''
            if value == '0':
                self.zero = True

    def setPoints(self, value):
        if value in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            self.points = int(value)
        elif value in ("W", "+4"):
            self.points = 50
        else:
            self.points = 20

    #############################################

    ### -\/-  Wild Card Methods  -\/- ###

    def changeColor(self, color):
        '''Changes Card's Color, Intended for Wild Cards.'''
        self.setColor(color)

    def isWild(self):
        '''Returns if card is a wild card.'''
        return self.wild

    def isZero(self):
        return self.zero
