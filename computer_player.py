from player import Player
import random

class ComputerPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.type = 'Computer'
        self.colorsInHand = {'red': 0, 'blue': 0, 'green': 0, 'yellow': 0, 'wild': 0}
        self.colorsOutHand = {}
        self.currentColor = ""

    def addCard(self, card):
        Player.addCard(self, card)
        color = card.getColor()
        self.colorsInHand[color] += 1

    def indexCard(self, cardColor, cardValue):
        for card in self.hand:
            if card.getValue() == cardValue:
                if cardValue in ('+4', 'W'):
                    return self.hand.indexCard(card)
                else:
                    if card.getColor() == cardColor:
                        return self.hand.indexCard(card)
        raise ValueError("Card Cannot Be Found")

    def think(self, match):
        card = None
        self.currentColor = match.currentColor
        currentValue = match.currentValue
        zeroChangeRule = match.zeroChange
        twoPlayers = False
        previousTurnID = match.getNextTurn(True)
        nextTurnID = match.getNextTurn(False)
        previousPlayer = match.getPlayer(previousTurnID)
        nextPlayer = match.getPlayer(nextTurnID)
        if previousTurnID == nextTurnID:
            twoPlayers = True
            if self.canSkip == False and self.canReverse == True:
                self.canSkip = True
            self.canReverse = False

        self.getLegalCards(self.currentColor, currentValue, zeroChangeRule)

        ### DRAW CASE ###

        if len(self.legalCards) == 0 and len(self.wildCards) == 0:
            return "d"

        else:

            ### NO LEGAL CARD, USE WILD CARD ###

            if len(self.legalCards) == 0:

                if zeroChangeRule and self.canZeroChange:
                    bestZeroColor = self.getBestColor(self.zeroCards)
                    card = self.getCardByColor(self.zeroCards, bestZeroColor)

                else:

                    if self.canDrawFour:
                        card = self.getCardByValue(self.wildCards, "+4")
                        print(card)

                    else:
                        card = random.choice(self.wildCards)

            else:

                ### HAS LEGAL CARD ###

                if twoPlayers and self.canSkip:  # Always play a skip card in a two player game
                    # print("Shed Skip Strategy")
                    card = self.getCardByValue(self.legalCards, "R", "X")

                if self.canReverse and previousPlayer.didDraw():
                    # print("Reverse Strategy")
                    reverseCards = self.getAllCardsByValue(self.legalCards, "R")
                    for reverseCard in reverseCards:
                        if reverseCard.getColor() == self.currentColor:
                            card = reverseCard

                if self.canValueChange:
                    # Computer Can Value Change, However, Should it?
                    # Computer Checks to See if Value Change Color is Better Than Current
                    currentColorNum = self.colorsInHand[self.currentColor]
                    bestValueChangeColor = self.getBestColor(self.valueChangeCards)
                    if self.colorsInHand[bestValueChangeColor] > currentColorNum or len(self.valueChangeCards) == len(
                            self.legalCards):
                        card = self.getCardByColor(self.valueChangeCards, bestValueChangeColor)

                if card == None:
                    # print("Random Strategy")
                    card = random.choice(list(set(self.legalCards) - set(self.valueChangeCards)))

        color = card.getColor()
        self.colorsInHand[color] -= 1
        return str(self.indexCard(card.getColor(), card.getValue()))

    def getWildColor(self):
        maxKey = max(self.colorsInHand, key=self.colorsInHand.get)
        if maxKey == 'wild':
            return random.choice(('r', 'g', 'b', 'y'))
        else:
            return maxKey

    def getCardByValue(self, cardList, *values):
        for card in cardList:
            if card.getValue() in values:
                return card

    def getAllCardsByValue(self, cardList, *values):
        cards = []
        for card in cardList:
            if card.getValue() in values:
                cards.append(card)
        return cards

    def getCardByColor(self, cardList, *colors):
        for card in cardList:
            if card.getColor() in colors:
                return card

    def getBestColor(self, cardList):
        bestColor = None
        bestColorNum = 0
        for card in cardList:
            color = card.getColor()
            if self.colorsInHand[color] > bestColorNum:
                bestColor = color
                bestColorNum = self.colorsInHand[color]
        return bestColor
