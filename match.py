import math
import time
import os
import random
from deck import Deck
from card import Card
from game_settings import GameSettings

class Match():
    elementsInit = {
        ### Names (final) ###
        'P1Name': '           ', 'P2Name': '           ', 'P3Name': '           ', 'P4Name': '           ',
        ### Card Values ###
        'P1Cards': '           ', 'P2Cards': '           ', 'P3Cards': '           ', 'P4Cards': '           ',
        ### Turn Colors / Hand###
        'P1Turn': '', 'P2Turn': '', 'P3Turn': '', 'P4Turn': '',
        'HName': '\t\t', 'HVisual': '', 'Hand': '',
        ### Deck ###
        'DNum': '', 'Deck': ['', '', '', '', '', '', '', '', ''],
        'PostDNum': '',
        ### Pile ###
        'uHeader': '\t\t\t\t', 'uMiddle': '   ', 'uLower': '   ',
        'oHeader': '\t\t\t',
        'oMiddle': ['\t\t\t', '\t\t\t', '\t\t\t', '\t\t\t', '\t\t\t', '\t\t\t', '\t\t\t', '\t\t\t'],
        ### Messages ###
        'Console': '', 'Error': ''
    }

    speeds = {'slow': 2, 'normal': 1, 'fast': 0}

    def __init__(self, gs):
        ### Decks ###
        self.deck = Deck(True)
        self.pile = Deck(False)

        ### Player Information ###
        self.players = gs.players
        self.turnList = []
        self.handTitles = {'play1': '', 'play2': '', 'play3': '', 'play4': ''}

        ### Carry Information ###
        self.displayEffects = gs.displayEffects
        self.hideComputerHands = gs.hideComputerHands
        self.zeroChange = gs.zeroChange
        self.computerSpeed = self.speeds[gs.computerSpeed]
        self.simulation = gs.computerSimulation

        ### Data ###
        self.handPosition = 0  # For hand displays
        self.drawAmount = 0  # Used for force draws
        self.passes = 0  # Keep track of consecutive passes for emergency color change
        self.passMax = 0  # Max passes before color change
        self.turn = ''  # Current turn
        self.event = ''  # Wild, Reverse, Skip, etc
        self.wildColorChange = ''  # Specifies color to change wild card to
        self.currentColor = ''  # Current color
        self.currentValue = ''  # Current value
        self.winnerID = ''  # ID of Player who Won
        self.reverse = False  # Is turn order reversed
        self.turnComplete = False  # Is turn complete
        self.matchComplete = False  # Is the Game over?
        self.matchAbort = False  # Did the match conclude without a winner?
        self.forcedWild = False  # Force change wild

        ### Initialize Names / Cards / Deck (Assuming New Game) ###
        self.elements = dict(self.elementsInit)

        keyStringName = 'P{}Name'
        keyStringCards = 'P{}Cards'

        for i in self.players:
            self.elements[keyStringName.format(i[-1])] = self.players[i].getName() + (
            ' ' * (11 - len(self.players[i].getName())))
            self.elements[keyStringCards.format(i[-1])] = '  ' + (
            ' ' * (3 - len(str(self.players[i].getCardNum())))) + str(self.players[i].getCardNum()) + ' Cards'

        self.elements['DNum'] = len(self.deck)

        if len(str(len(self.deck))) < 2:
            self.elements['PostDNum'] = '\t'

        j = 8
        for i in range(int(math.ceil(len(self.deck) / 12))):
            self.elements['Deck'][j] = '='
            j -= 1

        for key in GameSettings.playerIdentities:
            try:
                self.buildHandString(key)
                self.turnList += [key]
            except KeyError:
                pass

        self.passMax = len(self.turnList)

    def clearShell(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def begin(self):
        self.elements['Console'] = 'Beginning Game, Press Enter.'
        print(self.drawScreen())
        self.enterBreak()
        self.eventDealCards()
        self.turn = random.choice(self.turnList)
        self.elements['Console'] = 'First turn will be {}. Press Enter.'.format(self.players[self.turn].getName())
        print(self.drawScreen(True))
        self.enterBreak()
        self.placeCard()
        self.elements['P{}Turn'.format(self.turn[-1])] = '\033[93m'
        if self.event == 'wild':
            self.eventWildCard()
        elif self.event == 'reverse':
            self.eventReverse()

    def end(self, gs):
        if not self.matchAbort:
            points = 0
            self.elements['P{}Turn'.format(self.turn[-1])] = ''
            self.elements['Console'] = '{} Wins! Press Enter to Begin Point Tally'.format(
                self.players[self.winnerID].getName())
            print(self.drawScreen())
            self.enterBreak()

            for identity in self.turnList:
                if identity != self.winnerID:
                    self.turn = identity
                    self.elements['HName'] = self.handTitles[self.turn]
                    self.elements['P{}Turn'.format(self.turn[-1])] = '\033[93m'
                    while self.players[identity].getCardNum() > 0:
                        card = self.players[identity].removeCard(0)
                        points += card.getPoints()
                        self.elements['Console'] = '{} Won {} Points!'.format(self.players[self.winnerID].getName(),
                                                                              points)

                        keyStringCards = 'P{}Cards'
                        self.elements[keyStringCards.format(identity[-1])] = '  ' + (
                        ' ' * (3 - len(str(self.players[identity].getCardNum())))) + str(
                            self.players[identity].getCardNum()) + ' Cards'
                        self.players[identity].maxScroll = math.ceil((self.players[identity].getCardNum() / 10) - 1)
                        if self.handPosition > self.players[identity].maxScroll:
                            self.handPosition -= 1
                        self.buildHandVisual(identity)

                        if self.displayEffects and not self.simulation:
                            print(self.drawScreen())
                            time.sleep(.1)
                    self.elements['P{}Turn'.format(self.turn[-1])] = ''

            self.players[self.winnerID].addPoints(points)
            self.elements['Console'] = '{} Won {} Points! Press Enter'.format(self.players[self.winnerID].getName(),
                                                                              points)
            print(self.drawScreen())
            self.enterBreak()

        gs.clearStaging()
        for identity in self.turnList:
            self.players[identity].discardHand()
            gs.addPlayer(self.players[identity])
        return gs

    def adjustCardAmount(self, playerID):
        keyStringCards = 'P{}Cards'
        self.elements[keyStringCards.format(playerID[-1])] = '  ' + (
        ' ' * (3 - len(str(self.players[playerID].getCardNum())))) + str(self.players[playerID].getCardNum()) + ' Cards'
        self.players[playerID].maxScroll = math.ceil((self.players[playerID].getCardNum() / 10) - 1)
        if self.handPosition > self.players[playerID].maxScroll:
            self.handPosition -= 1
        self.buildHandVisual(playerID)

    def buildHandString(self, playerID):
        playerName = self.players[playerID].getName()
        if len(playerName) < 9:
            self.handTitles[playerID] = "{}'s Hand\t".format(self.players[playerID].getName())
        else:
            self.handTitles[playerID] = "{}'s Hand".format(self.players[playerID].getName())

    def buildHandVisual(self, playerID):
        string = '['
        for i in range(self.players[playerID].maxScroll + 1):
            if i == self.handPosition:
                string += '|'
            else:
                string += '-'
        string += ']'
        self.elements['HVisual'] = string

    def checkInput(self, playerInput):
        if playerInput == '':
            return {'valid': False, 'entry': playerInput}
        if playerInput.isnumeric():
            if int(playerInput) + (10 * self.handPosition) < self.players[self.turn].getCardNum():
                return {'valid': True, 'entry': str(int(playerInput) + (10 * self.handPosition)), 'type': 'card'}
            else:
                self.elements['Error'] = '{} is not a card.'.format(playerInput)
                return {'valid': False, 'entry': playerInput}
        else:
            playerInput = playerInput.lower()[0]
            if playerInput in ['<', '>', 'u', 'd', 'p', 'q', 's']:
                return {'valid': True, 'entry': playerInput}
            else:
                self.elements['Error'] = '{} is not a valid selection.'.format(playerInput)
                return {'valid': False, 'entry': playerInput}

    def checkColorInput(self, playerInput):
        if playerInput == '':
            return {'valid': False, 'entry': playerInput}
        playerInput = str(playerInput).lower()[0]
        if playerInput[0] == 'b':
            return {'valid': True, 'entry': 'blue'}
        elif playerInput[0] == 'r':
            return {'valid': True, 'entry': 'red'}
        elif playerInput[0] == 'g':
            return {'valid': True, 'entry': 'green'}
        elif playerInput[0] == 'y':
            return {'valid': True, 'entry': 'yellow'}
        return {'valid': False, 'entry': playerInput}

    def eventDealCards(self):
        if self.displayEffects and not self.simulation:
            self.elements['Console'] = 'Dealing Cards...'
        for i in ('play1', 'play2', 'play3', 'play4'):
            if i in self.players:
                for j in range(7):
                    self.dealCard(i)
                    if self.displayEffects and not self.simulation:
                        print(self.drawScreen(True))
                        time.sleep(.1)

    def eventReverse(self):
        if self.displayEffects and not self.simulation:
            hide = False
            if self.players[self.turn].getType() == "Computer":
                hide = self.hideComputerHands
            self.elements['Console'] = "Reverse Card Played! Reversing Turn Order.".format(
                self.players[self.turn].getName())
            print(self.drawScreen(hide))
            time.sleep(1)
            for i in range(10):
                cardBigNums = self.pile[0].getBigNum(self.reverse, i)
                self.elements['oMiddle'] = cardBigNums
                print(self.drawScreen(hide))
                if self.displayEffects and not self.simulation:
                    time.sleep(.1)
        cardBigNums = self.pile[0].getBigNum(self.reverse, 9)
        self.elements['oMiddle'] = cardBigNums
        self.reverse = not self.reverse
        self.event = ''

    def eventSkip(self):
        if self.displayEffects and not self.simulation:
            hide = False
            if self.players[self.turn].getType() == "Computer":
                hide = self.hideComputerHands
            self.elements['Console'] = "Skip Card Placed! Skipping {}'s Turn.".format(self.players[self.turn].getName())
            print(self.drawScreen(hide))
            time.sleep(1)
            for i in range(2):
                self.elements['P{}Turn'.format(self.turn[-1])] = '\033[91m'
                print(self.drawScreen(hide))
                time.sleep(.3)
                self.elements['P{}Turn'.format(self.turn[-1])] = ''
                print(self.drawScreen(hide))
                time.sleep(.3)
        self.turnComplete = True
        self.event = ''

    def eventWildCard(self):
        hide = False
        if not self.forcedWild:
            if self.players[self.turn].getType() == 'Human':
                self.elements['Console'] = 'Wild Card! Specifiy a Color: (B)lue, (R)ed, (G)reen, (Y)ellow'
                self.elements['Error'] = 'Specifiy A Color'
                print(self.drawScreen())
                playerInput = str(input("Color Change: "))
                checked = self.checkColorInput(playerInput)
                while not checked['valid']:
                    if checked['entry'] == '<':
                        self.handPosition -= 1
                        if self.handPosition == -1:
                            self.handPosition = self.players[self.turn].maxScroll
                        self.buildHandVisual(self.turn)
                    elif checked['entry'] == '>':
                        self.handPosition += 1
                        if self.handPosition > self.players[self.turn].maxScroll:
                            self.handPosition = 0
                        self.buildHandVisual(self.turn)
                    print(self.drawScreen())
                    playerInput = str(input("Color Change: "))
                    checked = self.checkColorInput(playerInput)
            else:
                hide = self.hideComputerHands
                checked = self.checkColorInput(self.players[self.turn].getWildColor())
            self.wildColorChange = checked['entry']
        else:
            self.wildColorChange = self.checkColorInput(random.choice(('r', 'b', 'g', 'y')))['entry']
            self.forcedWild = False
        self.currentColor = self.wildColorChange
        self.elements['Error'] = ""
        if self.displayEffects and not self.simulation:
            self.elements['Console'] = 'Wild Card! Changing Color.'
            seed = 1
            for i in range(10):
                if seed > 4:
                    seed = 1
                print(self.drawScreen(hide, wildSeed=seed))
                time.sleep(.1)
                seed += 1
        self.pile[0].changeColor(self.wildColorChange)
        self.wildColorChange = ''
        cardBigNums = self.pile[0].getBigNum(self.reverse)
        self.elements['oHeader'] = '{}\u2666\u2666\u2666=========\u2666\u2666\u2666\033[0m\t'.format(
            self.pile[0].getColorCode())
        self.elements['oMiddle'] = cardBigNums
        self.event = ''

    def eventDraw(self):
        self.players[self.turn].addForceDraw(self.drawAmount)
        self.drawAmount = 0
        self.event = ''

    def dealCard(self, playerID):

        card = self.deck.draw()
        self.players[playerID].addCard(card)

        ### Adjust Hand Visual ###
        self.players[playerID].maxScroll = math.ceil((self.players[playerID].getCardNum() / 10) - 1)
        self.handPosition = self.players[playerID].maxScroll
        self.buildHandVisual(playerID)

        ### Adjust Player Tile ###
        keyStringCards = 'P{}Cards'
        self.elements[keyStringCards.format(playerID[-1])] = '  ' + (
        ' ' * (3 - len(str(self.players[playerID].getCardNum())))) + str(self.players[playerID].getCardNum()) + ' Cards'

        ### Adjust Deck ###
        self.elements['DNum'] = len(self.deck)
        if len(str(len(self.deck))) < 2:
            self.elements['PostDNum'] = '\t'
        j = 8
        self.elements['Deck'] = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        for i in range(math.ceil(len(self.deck) / 12)):
            self.elements['Deck'][j] = '='
            j -= 1

    def placeCard(self, card=None):
        if card == None:
            ### Used At Beginning For First Card ###
            card = self.deck.draw()
            card = Card('wild','W')
            self.elements['DNum'] = len(self.deck)

        cardColor = card.getColorCode()
        cardBigNums = card.getBigNum(self.reverse)

        self.currentColor = card.getColor()
        self.currentValue = card.getValue()

        self.pile.insert(card)
        self.elements['oHeader'] = '{}\u2666\u2666\u2666=========\u2666\u2666\u2666\033[0m\t'.format(cardColor)
        self.elements['oMiddle'] = cardBigNums

        if len(self.pile) > 1:
            previousCard = self.pile[1]
            previousCardColor = previousCard.getColorCode()
            self.elements['uHeader'] = '{}      \u2666\u2666\u2666=========\u2666\u2666\u2666\033[0m\t\t'.format(
                previousCardColor)
            self.elements['uMiddle'] = '{}| |\033[0m'.format(previousCardColor)
            self.elements['uLower'] = '{}\u2666\u2666\u2666\033[0m'.format(previousCardColor)

        if self.currentColor == 'wild':
            self.event = 'wild'

        if self.currentValue == 'X':
            self.event = 'skip'
        elif self.currentValue == 'R':
            if len(self.players) > 2:
                self.event = 'reverse'
            else:
                self.event = 'skip'
        elif self.currentValue == '+4':
            self.drawAmount = 4
        elif self.currentValue == '+2':
            self.drawAmount = 2
        self.passes = 0

    def extractCard(self, playerID, index):
        card = self.players[playerID].removeCard(index)
        if self.players[playerID].getCardNum() == 0:
            self.matchComplete = True
            self.winnerID = self.turn
        self.adjustCardAmount(playerID)
        return card

    def enterBreak(self):
        if not self.simulation:
            str(input())
        return

    def nextTurn(self):
        self.turnComplete = False
        self.handPosition = 0
        turnType = self.players[self.turn].getType()
        self.players[self.turn].beginTurn()
        ### Prepare Hand Visuals ###

        self.elements['HName'] = self.handTitles[self.turn]
        self.buildHandVisual(self.turn)

        if self.event == 'skip':
            self.eventSkip()
        elif self.drawAmount > 0:
            self.eventDraw()

        while not self.turnComplete:
            if turnType == 'Human':
                self.players[self.turn].getLegalCards(self.currentColor, self.currentValue, self.zeroChange)
                if len(self.deck) > 0:
                    self.elements['Console'] = 'Select a card, (D)raw, or (P)ause.'
                else:
                    self.players[self.turn].removeForceDraw()
                    self.elements['Console'] = 'Select a card, (D)raw, (P)ause, or Pas(s).'
                if self.players[self.turn].getForceDraws() > 0:
                    self.elements['Error'] = 'Draw Card Played! Draw {} cards.'.format(
                        self.players[self.turn].getForceDraws())
                print(self.drawScreen())
                playerInput = str(input("\033[97mSelection: \033[92m"))
                checked = self.checkInput(playerInput)
                while not checked['valid']:
                    print(self.drawScreen())
                    playerInput = str(input("\033[97mSelection: \033[92m"))
                    checked = self.checkInput(playerInput)

                playerInput = checked['entry']

                if playerInput == '<':
                    self.handPosition -= 1
                    if self.handPosition == -1:
                        self.handPosition = self.players[self.turn].maxScroll
                    self.buildHandVisual(self.turn)
                elif playerInput == '>':
                    self.handPosition += 1
                    if self.handPosition > self.players[self.turn].maxScroll:
                        self.handPosition = 0
                    self.buildHandVisual(self.turn)
                elif playerInput == 'd':
                    if len(self.deck) > 0:
                        self.elements['Error'] = ''
                        self.dealCard(self.turn)
                    else:
                        self.elements['Error'] = "Cannot Draw. Deck is Empty"
                elif playerInput == 'p':
                    pauseOutput = self.pauseScreen()
                    if pauseOutput == 'quit':
                        self.matchComplete = True
                        self.turnComplete = True
                        self.winnerID = 'play1'
                        self.matchAbort = True
                elif playerInput == 's':
                    if len(self.deck) > 0:
                        self.elements['Error'] = "Cannot pass until Deck is empty."
                    elif len(self.players[self.turn].getAllValidCards()) > 0:
                        self.elements['Error'] = "Cannot pass while having playable cards."
                    else:
                        self.turnComplete = True
                        self.passes += 1
                        if self.passes == self.passMax:
                            self.forcedWild = True
                            self.event = 'wild'
                            self.passes = 0
                elif playerInput.isnumeric():
                    if self.players[self.turn].getForceDraws() == 0:
                        cardCheck = self.players[self.turn].checkCard(playerInput)
                        if cardCheck in self.players[self.turn].getAllValidCards():
                            card = self.extractCard(self.turn, playerInput)
                            self.placeCard(card)
                            self.elements['Error'] = ""
                            self.turnComplete = True
                        else:
                            self.elements['Error'] = "Card Doesn't Match The Color {} or Value {}!".format(
                                self.currentColor, self.currentValue)
                    else:
                        pass

            elif turnType == 'Computer':
                self.elements['Console'] = '{}\'s Turn'.format(self.players[self.turn].getName())
                print(self.drawScreen(self.hideComputerHands))
                if not self.simulation:
                    time.sleep(self.computerSpeed)
                # str(input())
                while (True):
                    if self.displayEffects and not self.simulation:
                        time.sleep(.2)
                    if self.players[self.turn].getForceDraws() > 0 and len(self.deck) > 0:
                        cardIndex = 'd'
                    else:
                        cardIndex = self.players[self.turn].think(self)
                    if cardIndex.isnumeric():
                        card = self.extractCard(self.turn, int(cardIndex))
                        if card.getColor() != self.currentColor:
                            self.resetDrawBool()
                        self.placeCard(card)
                        self.turnComplete = True
                        break
                    else:
                        if cardIndex == 'd':
                            if len(self.deck) > 0:
                                self.dealCard(self.turn)
                                print(self.drawScreen(self.hideComputerHands))
                            else:
                                self.turnComplete = True
                                self.players[self.turn].removeForceDraw()
                                self.passes += 1
                                if self.passes == self.passMax:
                                    self.forcedWild = True
                                    self.event = 'wild'
                                    self.passes = 0
                                break

                                ### DECODE INPUT ###

        if self.event == 'reverse':
            self.eventReverse()
        elif self.event == 'wild':
            self.eventWildCard()

        # Clear Current Turn
        self.elements['P{}Turn'.format(self.turn[-1])] = ''
        # Prepare Next Turn
        self.turn = self.getNextTurn()
        self.elements['P{}Turn'.format(self.turn[-1])] = '\033[93m'

    def drawScreen(self, hide=False, wildSeed=0):
        if self.simulation:
            return ''
        colorCombos = {
            1: ['\033[91m', '\033[93m', '\033[92m', '\033[94m'],
            2: ['\033[94m', '\033[91m', '\033[93m', '\033[92m'],
            3: ['\033[92m', '\033[94m', '\033[91m', '\033[93m'],
            4: ['\033[93m', '\033[92m', '\033[94m', '\033[91m']}
        currentTurn = self.turn
        if currentTurn == '':
            currentTurn = self.turnList[-1]
            hide = True
        if wildSeed != 0:
            colorMod = colorCombos[wildSeed]
        else:
            colorMod = ['', '', '', '']

        self.clearShell()
        screenout = ''
        screenout += '\t\t\033[94m      || ||\033[92m ||\ ||  \033[91m// \\\\\n\033[0m'
        screenout += '\t\t\033[94m      || ||\033[92m ||\\\|| \033[91m((   ))\n\033[0m'
        screenout += '\t\t\033[94m      \\\ //\033[92m || \|| \033[91m \\\ //\n\033[0m'
        screenout += '\033[97m===============================================================\n'
        screenout += '\033[93m{}\033[0m\n'.format(self.elements['Console'])
        screenout += '\033[97m===============================================================\n'
        screenout += '\t\t\t\t\t\t' + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P1Turn'])
        screenout += '\033[97mDeck:\t\t' + '{}'.format(self.elements['uHeader']) + ' \033[97m{}|{}|\033[0m\n'.format(
            self.elements['P1Turn'], self.elements['P1Name'])
        screenout += '\033[97m{} Cards'.format(self.elements['DNum']) + '{}'.format(
            self.elements['PostDNum']) + '\t' + '{}'.format(
            self.elements['uHeader']) + ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P1Turn'],
                                                                          self.elements['P1Cards'])
        screenout += '\t\t      ' + '{}'.format(self.elements['uMiddle']) + '\033[97m{}{}'.format(colorMod[0],
                                                                                                  self.elements[
                                                                                                      'oHeader']) + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(
            self.elements['P1Turn'])
        screenout += '\033[97m  _+_ \t\t      ' + '{}'.format(self.elements['uMiddle']) + '\033[97m{}{}'.format(
            colorMod[1], self.elements['oHeader']) + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(
            self.elements['P2Turn'])
        screenout += '\033[97m | ' + '\033[92m{}\033[0m'.format(
            self.elements['Deck'][0]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uMiddle']) + '\033[97m{}{}'.format(colorMod[2], self.elements['oMiddle'][
            0]) + ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P2Turn'], self.elements['P2Name'])
        screenout += '\033[97m | ' + '\033[92m{}\033[0m'.format(
            self.elements['Deck'][1]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uMiddle']) + '\033[97m{}{}'.format(colorMod[3], self.elements['oMiddle'][
            1]) + ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P2Turn'], self.elements['P2Cards'])
        screenout += '\033[97m | ' + '\033[92m{}\033[0m'.format(
            self.elements['Deck'][2]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uMiddle']) + '\033[97m{}{}'.format(colorMod[0], self.elements['oMiddle'][
            2]) + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P2Turn'])
        screenout += '\033[97m | ' + '\033[93m{}\033[0m'.format(
            self.elements['Deck'][3]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uMiddle']) + '\033[97m{}{}'.format(colorMod[1], self.elements['oMiddle'][
            3]) + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P3Turn'])
        screenout += '\033[97m | ' + '\033[93m{}\033[0m'.format(
            self.elements['Deck'][4]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uMiddle']) + '\033[97m{}{}'.format(colorMod[2], self.elements['oMiddle'][
            4]) + ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P3Turn'], self.elements['P3Name'])
        screenout += '\033[97m | ' + '\033[93m{}\033[0m'.format(
            self.elements['Deck'][5]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uMiddle']) + '\033[97m{}{}'.format(colorMod[3], self.elements['oMiddle'][
            5]) + ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P3Turn'], self.elements['P3Cards'])
        screenout += '\033[97m | ' + '\033[91m{}\033[0m'.format(
            self.elements['Deck'][6]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uLower']) + '\033[97m{}{}'.format(colorMod[0], self.elements['oMiddle'][
            6]) + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P3Turn'])
        screenout += '\033[97m | ' + '\033[91m{}\033[0m'.format(
            self.elements['Deck'][7]) + '\033[97m |\t\t      ' + '{}'.format(
            self.elements['uLower']) + '\033[97m{}{}'.format(colorMod[1], self.elements['oMiddle'][
            7]) + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P4Turn'])
        screenout += '\033[97m |_' + '\033[91m{}\033[0m'.format(
            self.elements['Deck'][8]) + '\033[97m_|\t\t         ' + '\033[97m{}{}'.format(colorMod[2], self.elements[
            'oHeader']) + ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P4Turn'], self.elements['P4Name'])
        screenout += '\033[97m\t\t         ' + '\033[97m{}{}'.format(colorMod[3], self.elements[
            'oHeader']) + ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P4Turn'], self.elements['P4Cards'])
        screenout += '\t\t\t\t\t\t' + ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P4Turn'])
        screenout += "\033[97m{}".format(self.elements['HName']) + "\t\t\t\t {}\n".format(self.elements['HVisual'])
        screenout += '\033[97m===============================================================\n'
        screenout += self.players[currentTurn].getHand(self.handPosition, hide)
        screenout += '\033[91m{}\033[0m'.format(self.elements['Error'])
        return screenout

    def pauseScreen(self):
        while True:
            self.clearShell()
            print('\n\t\t\tPause')
            print('\n\t\t1. Resume')
            print('\t\t2. Quit')

            selection = str(input('\nSelection: ')).upper()
            while selection not in ['1', '2']:
                print('\nSelection Invalid')
                selection = str(input('\nSelection: ')).upper()

            if selection == '1' or "":
                return ""

            elif selection == '2':
                return "quit"

    def isComplete(self):
        return self.matchComplete

    def getNextTurn(self, forceReverse=False):
        if forceReverse:
            reverse = not self.reverse
        else:
            reverse = self.reverse
        currentIndex = self.turnList.index(self.turn)
        if not reverse:
            if (currentIndex + 1) == len(self.turnList):
                return self.turnList[0]
            else:
                return self.turnList[currentIndex + 1]
        else:
            if currentIndex == 0:
                return self.turnList[len(self.turnList) - 1]
            else:
                return self.turnList[currentIndex - 1]

    def getPlayer(self, playerID):
        return self.players[playerID]

    def resetDrawBool(self):
        for identity in self.players:
            self.players[identity].drew = False
