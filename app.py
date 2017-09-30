import os
import sys

from game_settings import GameSettings
from player import Player
from computer_player import ComputerPlayer
from match import Match

class BadInputError(Exception):
    pass

def Uno():

    def clearShell():
        os.system('cls' if os.name == 'nt' else 'clear')

    def mainMenu():
        sys.stdout.write("\x1b[8;32;63t")
        sys.stdout.flush()
        gs = GameSettings()

        while True:

            print(drawMainMenu(gs))

            selection = str(input('\033[97mSelection: \033[92m'))
            while selection not in ['1', '2', '3', '4', '5']:
                gs.mainMenuError = "Invalid Selection"
                print(drawMainMenu(gs))
                selection = str(input('\033[97mSelection: \033[92m'))

            if selection == '1':
                if gs.canBegin():
                    gs.mainMenuError = ""
                    gs.finalizePlayers()
                    gs = playMatch(gs)
                else:
                    gs.mainMenuError = "Two Players Required to Begin"

            elif selection == '2':
                if gs.canAddPlayer():
                    gs.mainMenuError = ""
                    gs = addPlayer(gs)
                else:
                    gs.mainMenuError = "Max Number of Players Reached"

            elif selection == '3':
                if gs.canAddPlayer():
                    gs.mainMenuError = ""
                    gs = addComputer(gs)
                else:
                    gs.mainMenuError = "Max Number of Players Reached"

            elif selection == '4':
                if gs.canRemovePlayer():
                    gs.mainMenuError = ""
                    gs = removePlayer(gs)
                else:
                    gs.mainMenuError = "No Players to Remove"

            elif selection == '5':
                gs.mainMenuError = ""
                gs = settingsMenu(gs)

            else:
                raise BadInputError('Data Provided Has No Function')

    def playMatch(gs):
        for i in range(1):
            m = Match(gs)
            m.begin()
            while not m.isComplete():
                m.nextTurn()
            gs = m.end(gs)
        return gs

    def addPlayer(gs):
        colors = ['\033[91m', '\033[94m', '\033[92m', '\033[93m']
        nameOkay = False
        playerNum = gs.getPlayerNum() + 1
        colorIndex = playerNum - 1
        message = "\033[97mPlease Enter Player {}'s Name: {}".format(playerNum, colors[colorIndex])

        while not nameOkay:
            print(drawMainMenu(gs))
            name = str(input(message)).title()
            if len(name) > 11:
                gs.mainMenuError = "Name Must Be 11 Characters or Less!"
            elif len(name) == 0:
                gs.mainMenuError = ""
                return gs
            else:
                nameOkay = True
                for player in gs.playerStaging:
                    if player.getName() == name:
                        nameOkay = False
                if nameOkay == False or name in GameSettings.computerNames:
                    gs.mainMenuError = "Name Cannot Match Another Player's Name!"

        p = Player(name)
        gs.addPlayer(p)
        gs.mainMenuError = ""

        return gs

    def addComputer(gs):
        name = gs.getComputerName()
        c = ComputerPlayer(name)
        gs.addPlayer(c)

        return gs

    def removePlayer(gs):
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=63))
        sys.stdout.flush()
        clearShell()

        complete = False
        playerNum = gs.getPlayerNum()
        message = "\033[97mPlease Enter Player Number to Remove: \033[91m".format(playerNum)

        while not complete:
            print(drawMainMenu(gs))
            number = str(input(message))
            if len(number) == 0:
                gs.mainMenuError = ""
                return gs
            try:
                number = int(number)
                if 0 < number <= playerNum:
                    complete = True
                else:
                    gs.mainMenuError = "Invalid Player Number!"
            except:
                gs.mainMenuError = "Please Enter the Player Number, not Name!"

        gs.mainMenuError = ""
        gs.removePlayer(number)
        return gs

    def settingsMenu(gs):
        while True:
            sys.stdout.write("\x1b[8;32;63t")
            sys.stdout.flush()
            clearShell()
            print('\n\t\tSettings')
            print('\n\t1. Draw Effects\t\t\t{}'.format(gs.displayEffects))
            print('\t2. Hide Computer Hands\t\t{}'.format(gs.hideComputerHands))
            print('\t3. Computer Speed\t\t{}'.format(gs.computerSpeed.title()))
            # print('\t4. Zero Card Changes Color\t{}'.format(gs.zeroChange))
            # print('\t5. Run Simulations\t\t{}'.format(gs.computerSimulation))
            print('\n\tA. Exit')

            selection = str(input('\nSelection: ')).upper()
            while selection not in ('1', '2', '3', '4', '5', 'A', ''):
                print('\nSelection Invalid')
                selection = str(input('\nSelection: ')).upper()

            if selection == '1':
                gs.displayEffects = not gs.displayEffects

            elif selection == '2':
                gs.hideComputerHands = not gs.hideComputerHands

            elif selection == '3':
                gs.changeComputerSpeed()
                '''
            elif selection == '4':
                gs.zeroChange = not gs.zeroChange

            elif selection == '5':
                gs.computerSimulation = not gs.computerSimulation
                '''
            elif selection == 'A' or selection == '' or selection in ('4', '5'):
                return gs

    def drawMainMenu(gs):
        clearShell()
        gs.compileMainMenuElements()
        menuElements = gs.getMainMenuElements()
        screenout = ''
        screenout += '\t\t\033[94m      || ||\033[92m ||\ ||  \033[91m// \\\\\n\033[0m'
        screenout += '\t\t\033[94m      || ||\033[92m ||\\\|| \033[91m((   ))\n\033[0m'
        screenout += '\t\t\033[94m      \\\ //\033[92m || \|| \033[91m \\\ //\n\033[0m'
        screenout += '\033[97m===============================================================\033[0m\n'
        screenout += "{}1-----------------------------1\033[0m {}2-----------------------------2\033[0m\n".format(
            menuElements['play1box'], menuElements['play2box'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play1box'], menuElements['play1row1'],
                                                            menuElements['play2box'], menuElements['play2row1'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play1box'], menuElements['play1row2'],
                                                            menuElements['play2box'], menuElements['play2row2'])
        screenout += "{}1-----------------------------1\033[0m {}2-----------------------------2\033[0m\n".format(
            menuElements['play1box'], menuElements['play2box'])
        screenout += "{}3-----------------------------3\033[0m {}4-----------------------------4\033[0m\n".format(
            menuElements['play3box'], menuElements['play4box'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play3box'], menuElements['play3row1'],
                                                            menuElements['play4box'], menuElements['play4row1'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play3box'], menuElements['play3row2'],
                                                            menuElements['play4box'], menuElements['play4row2'])
        screenout += "{}3-----------------------------3\033[0m {}4-----------------------------4\033[0m\n".format(
            menuElements['play3box'], menuElements['play4box'])
        screenout += "\033[97m===============================================================\033[0m\n"
        screenout += "  {}\u2666---------------------------\u2666\033[0m \u2666===========================\u2666\n".format(
            menuElements['beginBox'])
        screenout += "  {}|1.       Begin Match       |\033[0m |        High Scores        |\n".format(
            menuElements['beginBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m \u2666---------------------------\u2666\n".format(
            menuElements['beginBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(
            menuElements['addBox'])
        screenout += "  {}|2.       Add Player        |\033[0m |                           |\n".format(
            menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(
            menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(
            menuElements['addBox'])
        screenout += "  {}|3.      Add Computer       |\033[0m |                           |\n".format(
            menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(
            menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(
            menuElements['removeBox'])
        screenout += "  {}|4.      Remove Player      |\033[0m |                           |\n".format(
            menuElements['removeBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(
            menuElements['removeBox'])
        screenout += "  \033[97m\u2666---------------------------\u2666\033[0m |                           |\n"
        screenout += "  \033[97m|5.        Settings         |\033[0m |                           |\n"
        screenout += "  \033[97m\u2666---------------------------\u2666\033[0m \u2666===========================\u2666\n"
        screenout += "\033[97m===============================================================\033[0m\n"
        screenout += '\033[91m{}\033[0m'.format(gs.mainMenuError)
        return screenout

    mainMenu()


if __name__ == "__main__":
    Uno()
