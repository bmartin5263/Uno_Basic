import random

class GameSettings():
    playerIdentities = ('play1', 'play2', 'play3', 'play4')
    computerNames = ('Watson', 'SkyNet', 'Hal', 'Metal Gear')

    def __init__(self):
        self.playerStaging = []  # Where Player Objs Are Stored Before Game Starts
        self.players = {}  # ID : Player Obj
        self.numPlayers = 0
        self.useColor = True
        self.displayEffects = True
        self.hideComputerHands = True
        self.zeroChange = False
        self.computerSimulation = False
        self.mainMenuError = ''
        self.computerSpeed = 'normal'

    def canAddPlayer(self):
        return self.numPlayers < 4

    def canRemovePlayer(self):
        return self.numPlayers > 0

    def canBegin(self):
        return self.numPlayers > 1

    def addPlayer(self, player):
        self.playerStaging.append(player)
        self.numPlayers += 1

    def removePlayer(self, number):
        number -= 1
        del self.playerStaging[number]
        self.numPlayers -= 1

    def clearStaging(self):
        self.numPlayers = 0
        self.playerStaging = []

    def finalizePlayers(self):
        self.players.clear()
        identity = 0
        for player in self.playerStaging:
            playerID = self.playerIdentities[identity]
            player.assignID(playerID)
            self.players[playerID] = player
            identity += 1

    def getPlayerNum(self):
        return self.numPlayers

    def getComputerName(self):
        complete = False
        index = self.numPlayers
        while not complete:
            name = self.computerNames[index]
            complete = True
            for player in self.playerStaging:
                if player.getName() == name:
                    index += 1
                    if index >= len(self.computerNames):
                        index = 0
                        complete = False

        return self.computerNames[index]

    def getRandomIdentity(self):
        '''For Getting a Random Player for First Turn.'''
        return random.choice(self.players.keys())

    def compileMainMenuElements(self):
        def getBlankSpace(word, total):
            return " " * (total - len(word))

        def getPlayerBox(playerNum, rowNum):
            if rowNum == 1:
                name = self.playerStaging[playerNum - 1].getName()
                return '{}{}'.format(name, getBlankSpace(name, 29))
            elif rowNum == 2:
                points = self.playerStaging[playerNum - 1].getPoints()
                return 'Points: {}{}'.format(points, getBlankSpace(str(points), 21))

        self.mainMenuElements = {'play1row1': 'No Player                    ',
                                 'play1row2': '                             ',
                                 'play2row1': 'No Player                    ',
                                 'play2row2': '                             ',
                                 'play3row1': 'No Player                    ',
                                 'play3row2': '                             ',
                                 'play4row1': 'No Player                    ',
                                 'play4row2': '                             ',
                                 'play1box': '\033[90m', 'play2box': '\033[90m', 'play3box': '\033[90m',
                                 'play4box': '\033[90m',
                                 'beginBox': '\033[90m', 'addBox': '\033[97m', 'removeBox': '\033[90m'
                                 }
        playerBoxKey = 'play{}box'
        playerRowKey = 'play{}row{}'
        i = 1
        for j in self.playerStaging:
            colorCode = ['\033[91m', '\033[94m', '\033[92m', '\033[93m']
            key = playerBoxKey.format(i)
            self.mainMenuElements[key] = colorCode[i - 1]
            self.mainMenuElements[playerRowKey.format(i, 1)] = getPlayerBox(i, 1)
            self.mainMenuElements[playerRowKey.format(i, 2)] = getPlayerBox(i, 2)
            i += 1
        if self.canBegin():
            self.mainMenuElements['beginBox'] = '\033[95m'
        if not self.canAddPlayer():
            self.mainMenuElements['addBox'] = '\033[90m'
        if self.canRemovePlayer():
            self.mainMenuElements['removeBox'] = '\033[97m'

    def changeComputerSpeed(self):
        if self.computerSpeed == 'slow':
            self.computerSpeed = 'normal'
        elif self.computerSpeed == 'normal':
            self.computerSpeed = 'fast'
        elif self.computerSpeed == 'fast':
            self.computerSpeed = 'slow'

    def getMainMenuElements(self):
        return self.mainMenuElements

