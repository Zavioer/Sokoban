import json
import re
import os
import time
import pygame
from . import logic
from random import randrange
from settings import *


class Menu:
    def __init__(self, game):
        """
        Class which represents the menu.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        self.game = game
        self.runDisplay = True
        self.pointerRect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100
        self.storekeeperImg = pygame.transform.scale(STOREKEEPER_IMG, (70, 70))

    def drawPointer(self):
        """
        Method that draws the pointer on the display.
        """
        self.game.display.blit(self.storekeeperImg, (self.pointerRect.x - 200,
                                                     self.pointerRect.y - 30))

    def blitScreen(self):
        """
        Method that updates the screen, resets the keys and blits the display on
        the window.
        """
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.resetKeys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        """
        Class which represents the main menu, inheriting from the Menu class.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        self.state = "Start"
        self.logoMenuX, self.logoMenuY = midWidth, midHeight - 220
        self.startMenuX, self.startMenuY = midWidth, midHeight - 40
        self.moduleMenuX, self.moduleMenuY = midWidth, midHeight + 30
        self.instructionsMenuX, self.instructionsMenuY = midWidth, midHeight + 100
        self.rankingMenuX, self.rankingMenuY = midWidth, midHeight + 170
        self.creditsMenuX, self.creditsMenuY = midWidth, midHeight + 240
        self.quitMenuX, self.quitMenuY = midWidth, midHeight + 310
        self.pointerRect.midtop = (self.startMenuX + self.offset, self.startMenuY)

    def displayMenu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True
        self.resetPointer()

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('SOKOBAN', 130, self.logoMenuX, self.logoMenuY,
                               WHITE, self.game.fontTitle)
            self.game.drawText('Start Game', 70, self.startMenuX, self.startMenuY,
                               WHITE, self.game.fontName)
            self.game.drawText('Load Game', 70, self.moduleMenuX, self.moduleMenuY,
                               WHITE, self.game.fontName)
            self.game.drawText('Instructions', 70, self.instructionsMenuX, self.instructionsMenuY,
                               WHITE, self.game.fontName)
            self.game.drawText('Ranking', 70, self.rankingMenuX, self.rankingMenuY,
                               WHITE, self.game.fontName)
            self.game.drawText('Credits', 70, self.creditsMenuX, self.creditsMenuY,
                               WHITE, self.game.fontName)
            self.game.drawText('Quit', 70, self.quitMenuX, self.quitMenuY,
                               WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def resetPointer(self):
        """
        Utility function for reset pointer position after selected action.
        """
        self.pointerRect.midtop = (self.startMenuX + self.offset, self.startMenuY)
        self.state = 'Start'

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an
        end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            if self.state == 'Start':
                self.pointerRect.midtop = (self.moduleMenuX + self.offset,
                                           self.moduleMenuY)
                self.state = 'Level'
            elif self.state == 'Level':
                self.pointerRect.midtop = (self.instructionsMenuX + self.offset,
                                           self.instructionsMenuY)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.pointerRect.midtop = (self.rankingMenuX + self.offset,
                                           self.rankingMenuY)
                self.state = 'Ranking'
            elif self.state == 'Ranking':
                self.pointerRect.midtop = (self.creditsMenuX + self.offset,
                                           self.creditsMenuY)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.pointerRect.midtop = (self.quitMenuX + self.offset,
                                           self.quitMenuY)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.pointerRect.midtop = (self.startMenuX + self.offset,
                                           self.startMenuY)
                self.state = 'Start'
        elif self.game.UP_KEY or self.game.W_KEY:
            if self.state == 'Start':
                self.pointerRect.midtop = (self.quitMenuX + self.offset,
                                           self.quitMenuY)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.pointerRect.midtop = (self.creditsMenuX + self.offset,
                                           self.creditsMenuY)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.pointerRect.midtop = (self.rankingMenuX + self.offset,
                                           self.rankingMenuY)
                self.state = 'Ranking'
            elif self.state == 'Ranking':
                self.pointerRect.midtop = (self.instructionsMenuX + self.offset,
                                           self.instructionsMenuY)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.pointerRect.midtop = (self.moduleMenuX + self.offset,
                                           self.moduleMenuY)
                self.state = 'Level'
            elif self.state == 'Level':
                self.pointerRect.midtop = (self.startMenuX + self.offset,
                                           self.startMenuY)
                self.state = 'Start'

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu depending on
        whether player has given its nickname.
        """
        self.movePointer()

        if self.game.START_KEY:
            if self.state == 'Start' and len(self.game.playerName) == 0:
                self.game.previousMenu = 'Start'
                self.game.currentMenu = self.game.inputMenu
            elif self.state == 'Start' and len(self.game.playerName) > 0:
                self.game.START_KEY = False
                self.game.currentMenu = self.game.moduleMenu
            elif self.state == 'Level' and len(self.game.playerName) == 0:
                self.game.previousMenu = 'Level'
                self.game.currentMenu = self.game.inputMenu
            elif self.state == 'Level':
                self.game.START_KEY = False
                self.game.currentMenu = self.game.loadSaveMenu
            elif self.state == 'Instructions':
                self.game.currentMenu = self.game.instructionsMenu
            elif self.state == 'Ranking':
                self.game.currentMenu = self.game.rankMenu
            elif self.state == 'Credits':
                self.game.currentMenu = self.game.creditsMenu
            elif self.state == 'Quit':
                self.game.running = False

            self.runDisplay = False


class ModuleMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the module menu, inheriting from the Menu class.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.firstModuleX, self.firstModuleY = midWidth, midHeight
        self.secondModuleX, self.secondModuleY = midWidth, midHeight + 100
        self.thirdModuleX, self.thirdModuleY = midWidth, midHeight + 200
        self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
        self.state = 'One'

    def displayMenu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True
        self.resetPointer()

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('Choose module: ', 120, midWidth, midHeight - 200,
                               WHITE, self.game.fontName)
            self.game.drawText('Module 1', 80, self.firstModuleX, self.firstModuleY,
                               WHITE, self.game.fontName)
            self.game.drawText('Module 2', 80, self.secondModuleX, self.secondModuleY,
                               WHITE, self.game.fontName)
            self.game.drawText('Module 3', 80, self.thirdModuleX, self.thirdModuleY,
                               WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu. Supports
        three module selection logic.
        """
        self.movePointer()

        if self.game.BACK_KEY or self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False

        if self.game.START_KEY:
            if self.state == 'One':
                self.game.currentMenu = self.game.diffMenu

            elif self.state == 'Two':
                self.runDisplay = False
                self.game.logicState = True

                while self.game.gameLevel <= 20 and self.game.START_KEY:
                    self.game.currentLevel = self.game.gameLevel
                    boardName = str(self.game.currentLevel) + '.txt'

                    logic.startTheGame(self.game.window, boardName, self.game,
                                       self.game.gamePoints, MODULE_II)

                    self.game.logicState = True

            elif self.state == 'Three':
                self.game.currentMenu = self.game.widthHeightMenu

            self.runDisplay = False

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an
        end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:

            if self.state == 'One':
                self.pointerRect.midtop = (self.secondModuleX + self.offset,
                                           self.secondModuleY)
                self.state = 'Two'
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset,
                                           self.thirdModuleY)
                self.state = 'Three'
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.firstModuleX + self.offset,
                                           self.firstModuleY)
                self.state = 'One'

        elif self.game.UP_KEY or self.game.W_KEY:

            if self.state == 'One':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset,
                                           self.thirdModuleY)
                self.state = 'Three'
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.firstModuleX + self.offset,
                                           self.firstModuleY)
                self.state = 'One'
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.secondModuleX + self.offset,
                                           self.secondModuleY)
                self.state = 'Two'

    def resetPointer(self):
        """
        Utility function for reset pointer position after selected action.
        """
        self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
        self.state = 'One'

class CreditsMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the credits menu, inheriting from the Menu class.
        Shows the info about the game developers.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.creditsTitleX, self.creditsTitleY = midWidth, midHeight - 280
        self.firstAuthorX, self.firstAuthorY = midWidth, midHeight - 150
        self.secondAuthorX, self.secondAuthorY = midWidth, midHeight - 70
        self.partOneX, self.partOneY = midWidth, midHeight + 60
        self.partTwoX, self.partTwoY = midWidth, midHeight + 140
        self.partThreeX, self.partThreeY = midWidth, midHeight + 220
        self.copyrightX, self.copyrightY = WIDTH - 175, HEIGHT - 15

    def displayMenu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the
        drawText() method. It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('THE GAME HAS BEEN WRITTEN BY', 85, self.creditsTitleX,
                               self.creditsTitleY, WHITE, self.game.fontName)
            self.game.drawText('PIOTR BATOR', 70, self.firstAuthorX, self.firstAuthorY,
                               WHITE, self.game.fontName)
            self.game.drawText('GABRIEL BRZOSKWINIA', 70, self.secondAuthorX,
                               self.secondAuthorY, WHITE, self.game.fontName)
            self.game.drawText('AS A PART OF', 60, self.partOneX, self.partOneY,
                               WHITE, self.game.fontName)
            self.game.drawText('THE MOTOROLA SCIENCE CUP', 60, self.partTwoX,
                               self.partTwoY, RED, self.game.fontName)
            self.game.drawText('COMPETITION TASKS', 60, self.partThreeX,
                               self.partThreeY, WHITE, self.game.fontName)
            self.game.drawText('2021 © ALL RIGHTS RESERVED', 30, self.copyrightX,
                               self.copyrightY, WHITE, self.game.fontName)

            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if self.game.BACK_KEY:
            self.game.currentMenu = self.game.mainMenu

        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu

        if self.game.START_KEY:
            self.game.currentMenu = self.game.mainMenu

        self.runDisplay = False


class InstructionsMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the instructions menu, inheriting from the Menu class.
        It is an interface that presents the rules of the game and controls to the player.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.instructionsTextX, self.instructionsTextY = midWidth, midHeight - 280
        self.image = pygame.image.load('./src/img/controls.png')
        self.image = pygame.transform.scale(self.image, (500, 350))

    def displayMenu(self):
        """
        Method that displays the menu. It prints 3 buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.display.blit(self.image, (self.instructionsTextX - 250,
                                                self.instructionsTextY + 150))
            self.game.drawText('USE', 55, self.instructionsTextX - 450,
                               self.instructionsTextY, WHITE, self.game.fontName)
            self.game.drawText('WSAD', 55, self.instructionsTextX - 340,
                               self.instructionsTextY, RED, self.game.fontName)
            self.game.drawText('IN ORDER TO MOVE YOUR STOREKEEPER', 55,
                               self.instructionsTextX + 150, self.instructionsTextY, WHITE, self.game.fontName)

            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if self.game.BACK_KEY:
            self.game.currentMenu = self.game.mainMenu

        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu

        if self.game.START_KEY:
            self.game.currentMenu = self.game.legendMenu

        self.runDisplay = False


class LegendMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the legend menu, inheriting from the Menu class.
        The rules of the game are displayed here.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.legendTextX, self.legendTextY = midWidth, midHeight - 280

    def displayMenu(self):
        """
        Method that displays the menu. It prints 12 buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('RULES', 100, self.legendTextX, self.legendTextY,
                               WHITE, self.game.fontName)
            self.game.drawText('THE GOAL OF THIS GAME IS TO MOVE', 45,
                               self.legendTextX, self.legendTextY + 150, WHITE, self.game.fontName)
            self.game.drawText('AND CORRECTLY POSITION THE', 45, self.legendTextX - 180,
                               self.legendTextY + 220, WHITE, self.game.fontName)
            self.game.drawText('BOXES', 45, self.legendTextX + 150,
                               self.legendTextY + 220, RED, self.game.fontName)
            self.game.drawText('IN A WAREHOUSE.', 45, self.legendTextX + 365,
                               self.legendTextY + 220, WHITE, self.game.fontName)
            self.game.drawText('YOU WILL PLAY AS THE', 45, self.legendTextX - 300,
                               self.legendTextY + 290, WHITE, self.game.fontName)
            self.game.drawText('WAREHOUSE KEEPER', 45, self.legendTextX + 90,
                               self.legendTextY + 290, RED, self.game.fontName)
            self.game.drawText('AND TRY TO COPE', 45, self.legendTextX + 430,
                               self.legendTextY + 290, WHITE, self.game.fontName)
            self.game.drawText('WITH THE CHALLENGE, FACING', 45, self.legendTextX - 300,
                               self.legendTextY + 360, WHITE, self.game.fontName)
            self.game.drawText('60 MAPS', 45, self.legendTextX + 50, self.legendTextY + 360,
                               RED, self.game.fontName)
            self.game.drawText('OF VARYING DIFFICULTY.', 45, self.legendTextX + 350,
                               self.legendTextY + 360, WHITE, self.game.fontName)
            self.game.drawText('WE WISH YOU GOOD LUCK!', 45, self.legendTextX,
                               self.legendTextY + 500, WHITE, self.game.fontName)

            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if self.game.BACK_KEY:
            self.game.currentMenu = self.game.mainMenu

        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu

        if self.game.START_KEY:
            self.game.currentMenu = self.game.mainMenu

        self.runDisplay = False

class DiffMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the diffMenu, inheriting from the Menu class.
        Player can choose game difficulty here.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.diffTitleX, self.diffTitleY = midWidth, midHeight - 200
        self.easyX, self.easyY = midWidth, midHeight
        self.mediumX, self.mediumY = midWidth, midHeight + 100
        self.hardX, self.hardY = midWidth, midHeight + 200
        self.pointerRect.midtop = (self.easyX + self.offset, self.easyY)
        self.state = 'Easy'
        self.moved = 'No'

    def displayMenu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True
        if self.moved == 'No':
            self.resetPointer()

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)

            self.game.drawText('SELECT YOUR DIFFICULTY', 85, self.diffTitleX, self.diffTitleY, WHITE, self.game.fontName)
            self.game.drawText('EASY', 80, self.easyX, self.easyY, WHITE, self.game.fontName)
            self.game.drawText('MEDIUM', 80, self.mediumX, self.mediumY, WHITE, self.game.fontName)
            self.game.drawText('HARD', 80, self.hardX, self.hardY, WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.BACK_KEY:
            self.game.currentMenu = self.game.mainMenu
            self.moved = 'No'

        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.moved = 'No'

        if self.game.START_KEY:
            self.game.currentMenu = self.game.mainMenu
            self.moved = 'No'

        self.runDisplay = False

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        Depending on the chosen difficulty, the player draws a map from three fields.
        """
        if self.game.START_KEY:
            self.moved = 'No'
            if self.state == 'Easy':
                self.runDisplay = False
                self.game.logicState = True
                self.game.currentLevel = randrange(1, 20)
                boardName = str(self.game.currentLevel) + '.txt'

                logic.startTheGame(self.game.window, boardName, self.game,
                                   self.game.gamePoints, MODULE_I)

            elif self.state == 'Medium':
                self.runDisplay = False
                self.game.logicState = True
                self.game.currentLevel = randrange(21, 40)
                boardName = str(self.game.currentLevel) + '.txt'

                logic.startTheGame(self.game.window, boardName, self.game,
                                   self.game.gamePoints, MODULE_I)

            elif self.state == 'Hard':
                self.runDisplay = False
                self.game.logicState = True
                self.game.currentLevel = randrange(41, 60)
                boardName = str(self.game.currentLevel) + '.txt'

                logic.startTheGame(self.game.window, boardName, self.game,
                                   self.game.gamePoints, MODULE_I)

        if self.game.DOWN_KEY or self.game.S_KEY:
            self.moved = 'Yes'
            if self.state == 'Easy':
                self.pointerRect.midtop = (self.mediumX + self.offset, self.mediumY)
                self.state = 'Medium'
            elif self.state == 'Medium':
                self.pointerRect.midtop = (self.hardX + self.offset, self.hardY)
                self.state = 'Hard'
            elif self.state == 'Hard':
                self.pointerRect.midtop = (self.easyX + self.offset, self.easyY)
                self.state = 'Easy'

        elif self.game.UP_KEY or self.game.W_KEY:
            self.moved = 'Yes'
            if self.state == 'Easy':
                self.pointerRect.midtop = (self.hardX + self.offset, self.hardY)
                self.state = 'Hard'
            elif self.state == 'Medium':
                self.pointerRect.midtop = (self.easyX + self.offset, self.easyY)
                self.state = 'Easy'
            elif self.state == 'Hard':
                self.pointerRect.midtop = (self.mediumX + self.offset, self.mediumY)
                self.state = 'Medium'

    def resetPointer(self):
        """
        Utility function for reset pointer position after selected action.
        """
        self.pointerRect.midtop = (self.easyX + self.offset, self.easyY)
        self.state = 'Easy'

class InputName(Menu):
    def __init__(self, game):
        """
        This is a class that handles user input. It gives its name, which is
        necessary for many functions in the game to work.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.inputNameX, self.inputNameY = midWidth, midHeight - 280

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if len(self.game.playerName) > 0 and self.game.START_KEY:
            self.runDisplay = False
            self.game.START_KEY = False
            self.game.running = True

            if self.game.previousMenu == 'Start':
                self.game.currentMenu = self.game.moduleMenu
            elif self.game.previousMenu == 'Level':
                self.game.currentMenu = self.game.loadSaveMenu

            self.game.previousMenu = ''

        elif self.game.ESC_PRESSED or self.game.BACK_KEY:
            self.runDisplay = False
            self.game.playerName = ''
            self.game.running = True
            self.game.currentMenu = self.game.mainMenu

    def inputName(self):
        """
        Function for handling player writing his nickname.
        """
        self.game.running = False

        event = pygame.event.poll()
        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)

            if len(key) == 1:
                if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and len(self.game.playerName) < 15:
                    self.game.playerName += key.upper()
                elif len(self.game.playerName) < 15:
                    self.game.playerName += key

            elif key == 'backspace':
                self.game.playerName = self.game.playerName[:len(self.game.playerName) - 1]
            elif key == 'return':
                self.game.START_KEY = True
            elif key == 'escape':
                self.game.ESC_PRESSED = True

        elif event.type == pygame.QUIT:
            self.runDisplay = False
            self.game.running = False

        self.game.drawText(self.game.playerName, 60, self.inputNameX, self.inputNameY + 350, RED,
                           self.game.fontName)
        self.game.drawText('Chars used: ' + str(len(self.game.playerName)), 30,
                           self.inputNameX, self.inputNameY + 600, WHITE, self.game.fontName)

    def displayMenu(self):
        """
        Method that displays the menu. It prints 2 buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.display.fill(BLACK)
            self.game.drawText('TYPE IN YOUR NICKNAME [15]', 95, self.inputNameX, self.inputNameY + 50, WHITE,
                               self.game.fontName)
            self.game.drawText('AND PRESS ENTER TO CONFIRM', 70, self.inputNameX, self.inputNameY + 150, WHITE,
                               self.game.fontName)

            self.inputName()
            self.checkInput()
            self.blitScreen()


class RankMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the rank menu, inheriting from the Menu class.
        The results are read from the file and a ranking of the players is being created.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.headerX = midWidth
        self.headerY = midHeight - 200
        self.itemY = midHeight - 100

    def displayMenu(self):
        """
        Method that displays the menu. It prints buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.checkEvents()

            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC_PRESSED:
                self.game.currentMenu = self.game.mainMenu
                self.runDisplay = False

            self.game.display.fill(BLACK)
            self.game.drawText('RANKING', 90, self.headerX, self.headerY, WHITE, self.game.fontName)

            def getScore(table):
                return table.get('userScore')

            with open('scoreFile.txt', 'r') as scoreFile:
                table = [json.loads(line) for line in scoreFile]
                counter = 1
                if len(table) == 0:
                    self.game.drawText('EMPTY RANKING', 100, self.headerX, self.itemY + 100, RED, self.game.fontName)
                else:
                    table.sort(key=getScore, reverse=True)

                    for row in table:
                        name = table[counter - 1]['userNameVar']
                        points = table[counter - 1]['userScore']
                        self.game.drawText('NAME', 60, self.headerX - 300, self.headerY + 100, WHITE, self.game.fontName)
                        self.game.drawText('POINTS', 60, self.headerX + 300, self.headerY + 100, WHITE, self.game.fontName)
                        if counter <= 5:
                            self.game.drawText(str(counter) + '. ' + str(name), 50, self.headerX - 300, self.itemY + (counter * 60), WHITE, self.game.fontName)
                            self.game.drawText(str(points), 50, self.headerX + 300, self.itemY + (counter * 60), RED, self.game.fontName)
                        counter += 1

                self.blitScreen()
        scoreFile.close()


class SaveGameMenu(Menu):
    def __init__(self, game):
        """
        Sub menu for game map and score saving to shelf file format.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.firstModuleX, self.firstModuleY = midWidth, midHeight
        self.secondModuleX, self.secondModuleY = midWidth, midHeight + 100
        self.thirdModuleX, self.thirdModuleY = midWidth, midHeight + 200
        self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
        self.state = 'Yes'

    def displayMenu(self):
        """
        Method that displays the menu. It prints buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True
        self.resetPointer()

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            if self.game.flagVar == MODULE_I:
                self.game.drawText('DO YOU WANT TO QUIT ?', 65, midWidth, midHeight - 300,
                                   WHITE, self.game.fontName)
            else:
                self.game.drawText('DO YOU WANT TO QUIT AND SAVE YOUR SCORE?', 65, midWidth, midHeight - 300,
                                   WHITE, self.game.fontName)
            self.game.drawText('YES', 60, self.firstModuleX, self.firstModuleY,
                               WHITE, self.game.fontName)
            self.game.drawText('NO', 60, self.secondModuleX, self.secondModuleY,
                               WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.START_KEY:
            if self.state == 'Yes':
                self.runDisplay = False
                self.game.START_KEY = False
                self.game.currentMenu = self.game.mainMenu

                if self.game.currentPlayerState['flag'] in [MODULE_II, MODULE_III, RESTORE]:
                    currLvl = self.game.currentLevel

                    logic.saveGame(self.game.currentPlayerState['width'],
                                   self.game.currentPlayerState['height'],
                                   self.game.currentPlayerState['sprites'],
                                   self.game.currentPlayerState['time'],
                                   self.game.playerName, currLvl, self.game.gamePoints,
                                   self.game.currentPlayerState['flag'])

                    if self.game.gameLevel > 1:
                        self.game.gameLevel = 1

                    self.game.gamePoints = 0

            if self.state == 'No':
                self.runDisplay = False
                self.game.currentMenu = self.game.mainMenu

        if self.game.ESC_PRESSED:
            self.runDisplay = False
            self.game.logicState = True

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            if self.state == 'Yes':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'No'
            elif self.state == 'No':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'Yes'
        elif self.game.UP_KEY or self.game.W_KEY:
            if self.state == 'Yes':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'No'
            elif self.state == 'No':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'Yes'

    def resetPointer(self):
        """
        Utility method for reset pointer to default position after action.
        """
        self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
        self.state = 'Yes'


class WidthHeightMenu(Menu):
    def __init__(self, game):
        """
        Sub menu for passing the width and height to 3rd module map-creator.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)

        self.textInfoX, self.textInfoY = midWidth, midHeight - 250
        self.widthX, self.widthY = midWidth, midHeight - 50
        self.heightX, self.heightY = midWidth, midHeight + 100
        self.nameX, self.nameY = midWidth - 300, midHeight + 220
        self.passedWidth = ''
        self.passedHeight = ''

        self.passiveColor = GRAY
        self.activeColor = LIGHTSKYBLUE
        self.inputWidthRect = pygame.Rect(self.widthX + 100, self.widthY - 50, 100, 100)
        self.inputHeightRect = pygame.Rect(self.heightX + 100, self.heightY - 50, 100, 100)
        self.inputNameRect = pygame.Rect(self.nameX + 100, self.nameY - 40, 450, 80)
        self.buttonWActive, self.buttonHActive, self.buttonNActive = False, False, False
        self.numberKeys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                           pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

        self.colorW = self.passiveColor
        self.colorH = self.passiveColor
        self.colorN = self.passiveColor

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.game.running = True
            self.runDisplay = False

        if self.game.START_KEY:
            if 8 <= int(self.passedWidth) <= 30 and 8 <= int(self.passedHeight) <= 20 and 0 < len(self.game.passedMapName) <= 15:
                self.runDisplay = False
                self.game.running = True
                self.game.logicState = True

                logic.createMap(self.game.window, int(self.passedWidth),
                                int(self.passedHeight), self.game)

                self.passedWidth = ''
                self.passedHeight = ''

    def inputHandle(self):
        """
        Method for handling input new created map width and height.
        """
        self.game.running = False

        event = pygame.event.poll()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.inputWidthRect.collidepoint(event.pos):
                self.buttonWActive = True
                self.colorW = self.activeColor
            elif not self.inputWidthRect.collidepoint(event.pos):
                self.buttonWActive = False
                self.colorW = self.passiveColor
            if self.inputHeightRect.collidepoint(event.pos):
                self.buttonHActive = True
                self.colorH = self.activeColor
            elif not self.inputHeightRect.collidepoint(event.pos):
                self.buttonHActive = False
                self.colorH = self.passiveColor
            if self.inputNameRect.collidepoint(event.pos):
                self.buttonNActive = True
                self.colorN = self.activeColor
            elif not self.inputNameRect.collidepoint(event.pos):
                self.buttonNActive = False
                self.colorN = self.passiveColor

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)

            if self.buttonWActive:
                if key == 'backspace':
                    self.passedWidth = self.passedWidth[:-1]
                elif key == 'return':
                    if len(self.passedHeight) > 0 and len(self.passedWidth) > 0:
                        self.game.START_KEY = True
                else:
                    if event.key in self.numberKeys and len(self.passedWidth) < 2:
                        self.passedWidth += event.unicode

            elif self.buttonHActive:
                if key == 'backspace':
                    self.passedHeight = self.passedHeight[:-1]

                elif key == 'return':
                    if len(self.passedHeight) > 0 and len(self.passedWidth) > 0:
                        self.game.START_KEY = True

                else:
                    if event.key in self.numberKeys and len(self.passedHeight) < 2:
                        self.passedHeight += event.unicode

            elif self.buttonNActive:
                if key == 'backspace':
                    self.game.passedMapName = self.game.passedMapName[:-1]

                elif key == 'return':
                    self.game.START_KEY = True

                else:
                    if len(self.game.passedMapName) < 15:
                        self.game.passedMapName += event.unicode

            elif key == 'return':
                if len(self.passedHeight) > 0 and len(self.passedWidth) > 0:
                    self.game.START_KEY = True

            elif key == 'escape':
                self.game.ESC_PRESSED = True

        elif event.type == pygame.QUIT:
            self.runDisplay = False
            self.game.running = False

        pygame.draw.rect(self.game.display, self.colorW, self.inputWidthRect, 2)
        pygame.draw.rect(self.game.display, self.colorH, self.inputHeightRect, 2)
        pygame.draw.rect(self.game.display, self.colorN, self.inputNameRect, 2)

        self.game.drawText(self.passedWidth, 50, self.widthX + 150, self.widthY,
                           WHITE, self.game.fontName)
        self.game.drawText(self.passedHeight, 50, self.heightX + 150, self.heightY,
                           WHITE, self.game.fontName)
        self.game.drawText(self.game.passedMapName, 40, self.nameX + 325, self.nameY,
                           WHITE, self.game.fontName)

    def displayMenu(self):
        """
        Method that displays the menu. It prints buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.display.fill(BLACK)

            self.game.drawText('ENTER YOUR MAP DIMENSIONS', 65, self.textInfoX,
                               self.textInfoY, WHITE, self.game.fontName)
            self.game.drawText('MIN: 8 x 8 MAX: 30 x 20 [press enter]', 35, self.textInfoX, self.textInfoY + 50,
                               RED, self.game.fontName)
            self.game.drawText('WIDTH: ', 60, self.widthX, self.widthY, WHITE,
                               self.game.fontName)
            self.game.drawText('HEIGHT: ', 60, self.heightX, self.heightY,
                               WHITE, self.game.fontName)
            self.game.drawText('NAME: ', 60, self.nameX, self.nameY,
                               WHITE, self.game.fontName)

            self.inputHandle()
            self.checkInput()
            self.blitScreen()

    def unableToSaveMonit(self):
        """
        Utility method for displaying short monit about information why map cant
        be saved.
        """
        self.game.display.fill(BLACK)
        self.game.drawText('Created map must have at least one of each game object.',
                           45, midWidth, midHeight - 45, WHITE, self.game.fontName)
        self.game.drawText('[Storekeeper, Box, Destination, Floor, Wall]',
                           45, midWidth, midHeight + 45, WHITE, self.game.fontName)
        self.blitScreen()
        time.sleep(2)

    def boxesDestinationInvalidMonit(self):
        """
        Utility method for displaying short monit about incorrect amounts of
        destinations and boxes
        """
        self.game.display.fill(BLACK)
        self.game.drawText('Created map must have equal or more amount',
                           45, midWidth, midHeight - 45, WHITE, self.game.fontName)
        self.game.drawText('of the Boxes than the Destinations amount.',
                           45, midWidth, midHeight + 45, WHITE, self.game.fontName)
        self.blitScreen()
        time.sleep(2)

    def tooManyBoardsMonit(self):
        """
        Utility method for displaying short monit if amount of player's own boards,
        exceed MAX_BOARD value.
        """
        self.game.display.fill(BLACK)
        self.game.drawText(f'You already have {MAX_BOARDS} maps. This is limit.',
                           45, midWidth, midHeight - 45, WHITE, self.game.fontName)
        self.game.drawText('Remove old one to save new.',
                           45, midWidth, midHeight + 45, WHITE, self.game.fontName)
        self.blitScreen()
        time.sleep(2)


class LoadMapMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        """
        Sub menu for Module III that allows player to choose his own map.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        self.textInfoX, self.textInfoY = midWidth - 25, midHeight - 280
        self.itemMapX, self.itemMapY = midWidth, midHeight - 200
        self.deleteRect = pygame.Rect(midWidth + 450, midHeight + 320, 140, 50)
        self.offset = -100
        self.pointerRect = pygame.Rect(0, 0, 20, 20)
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + 10)
        self.counter = 0
        self.storekeeperImg = pygame.transform.scale(STOREKEEPER_IMG, (40, 40))
        self.chosenMap = ''
        self.mapArray = []
        self.amount = 0

    def displayMenu(self):
        """
        Method that displays the menu. It also draws the pointer and blits the
        screen every single frame.
        """
        self.runDisplay = True
        self.resetPointer()

        maps = os.listdir(OWN_BOARDS_DIR)
        self.cleanMaps(maps)

        if len(self.mapArray) > 0:
            self.chosenMap = self.mapArray[0]

            while self.runDisplay:
                self.game.resetKeys()
                self.game.checkEvents()
                self.checkInput()

                self.game.display.fill(BLACK)
                self.game.drawText('CHOOSE MAP', 65, self.textInfoX, self.textInfoY,
                                   WHITE, self.game.fontName)

                for row in range(len(self.mapArray)):
                    if row < 12:
                        board = self.prepareMapName(self.mapArray[row])
                        self.game.drawText(str(board), 28, self.itemMapX, self.itemMapY + (row * 45),
                                           WHITE, self.game.fontName)

                self.drawPointer()
                self.blitScreen()
        else:
            while self.runDisplay:
                self.game.resetKeys()
                self.game.checkEvents()
                self.checkInput()

                self.game.display.fill(BLACK)
                self.game.drawText('YOU HAVE NOT CREATED A MAP YET', 65, midWidth, midHeight,
                                   WHITE, self.game.fontName)
                self.blitScreen()

    def resetPointer(self):
        """
        Utility function for reset pointer position after selected action.
        """
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + 10)
        self.chosenMap = ''

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            self.counter += 1

            if self.counter > len(self.mapArray) - 1 or self.counter > 11:
                self.counter = 0

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + (self.counter * 45))
            self.chosenMap = self.mapArray[self.counter]

        elif self.game.UP_KEY or self.game.W_KEY:
            self.counter -= 1

            if self.counter < 0:
                self.counter = len(self.mapArray) - 1

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + self.counter * 45)
            self.chosenMap = self.mapArray[self.counter]

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.ESC_PRESSED or self.game.BACK_KEY:
            self.runDisplay = False
            self.game.currentMenu = self.game.mainMenu
            self.counter = 0

            self.mapArray.clear()

        if self.game.START_KEY and len(self.mapArray) <= 0:
            self.runDisplay = False
            self.game.currentMenu = self.game.loadSaveMenu

            self.mapArray.clear()

        elif self.game.START_KEY and len(self.mapArray) > 0:
            self.runDisplay = False
            self.game.logicState = True
            self.counter = 0

            self.mapArray.clear()

            logic.startTheGame(self.game.window, self.chosenMap, self.game,
                               self.game.gamePoints, MODULE_III)

    def prepareMapName(self, fileName):
        """
        Utility function for preparing name of saved game.

        :param fileName:
            Name of file which contains map.
        :type fileName: str, required
        :return:
            Returns nice looking saved game file name.
        :rtype: str
        """
        mapName = fileName[:fileName.find('_')]
        date = fileName[len(mapName) + 1:]

        hours = date[:8]
        hours = hours.replace('_', ':')

        day = date[9: 19]
        day = day.replace('_', '/')

        result = ''.join((mapName.ljust(20, ' '), hours, '    ', day))

        return result

    def cleanMaps(self, maps):
        """
        Utility function for select only current playing player.

        :param maps:
            Name of maps to search in.
        :type maps: list, required
        """

        for file in maps:
            if re.search(rf'(.*)(_){self.game.playerName}\b(.*)', file):
                self.mapArray.append(file)


class DeleteMapMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        """
        Sub menu for Module III that allows player to delete his own map.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        self.textInfoX, self.textInfoY = midWidth, midHeight - 280
        self.itemMapX, self.itemMapY = midWidth, midHeight - 180

        self.offset = -100
        self.pointerRect = pygame.Rect(0, 0, 20, 20)
        self.storekeeperImg = pygame.transform.scale(STOREKEEPER_IMG, (40, 40))
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + 10)
        self.counter = 0
        self.mapArray = []
        self.chosenMap = ''

    def displayMenu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True
        self.resetPointer()

        for map in os.listdir(OWN_BOARDS_DIR):
            if map.find(self.game.playerName) > -1:
                self.mapArray.append(map)

        if len(self.mapArray) > 0:
            self.chosenMap = self.mapArray[0]

            while self.runDisplay:
                self.game.checkEvents()
                self.checkInput()

                self.game.display.fill(BLACK)
                self.game.drawText('DELETE YOUR MAP', 65, self.textInfoX, self.textInfoY,
                                   WHITE, self.game.fontName)

                for row in range(len(self.mapArray)):
                    if row < 12:
                        board = self.prepareSaveName(self.mapArray[row])
                        self.game.drawText(str(board), 28, self.itemMapX, self.itemMapY + (row * 45),
                                           WHITE, self.game.fontName)

                self.drawPointer()
                self.blitScreen()
        else:
            while self.runDisplay:
                self.game.checkEvents()
                self.checkInput()

                self.game.display.fill(BLACK)
                self.game.drawText('YOU HAVE NOT CREATED A MAP YET', 65, midWidth, midHeight,
                                   WHITE, self.game.fontName)

                self.blitScreen()

    def resetPointer(self):
        """
        Utility function for reset pointer position after selected action.
        """
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + 10)
        self.chosenMap = ''

    def prepareSaveName(self, filename):
        """
        Utility function for preparing player save game for nice format.

        :param filename:
            Name of the file which contains save.
        :type filename: str, required

        :return:
            Nice looking save game name.
        :rtype: str
        """
        playerName = filename[:filename.find('_')]
        hours = filename[len(playerName) + 1:]

        hour = hours[:8]
        date = hours[9:19]

        hour = hour.replace('_', ':')
        date = date.replace('_', '/')

        result = ''.join((playerName, '        ', hour, '    ', date))

        return result

    def removeMap(self, mapID):
        """
        Function for module III which allows player to delete his own map.

        :param mapID:
            ID of created map.
        :type mapID: int, required
        """
        if os.path.isfile('./src/boards/own/' + str(mapID)):
            os.remove('./src/boards/own/' + mapID)

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            self.counter += 1

            if self.counter > len(self.mapArray) - 1 or self.counter > 11:
                self.counter = 0

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + (self.counter * 45))
            self.chosenMap = self.mapArray[self.counter]

        elif self.game.UP_KEY or self.game.W_KEY:
            self.counter -= 1

            if self.counter < 0:
                self.counter = len(self.mapArray) - 1

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + self.counter * 45)
            self.chosenMap = self.mapArray[self.counter]

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.ESC_PRESSED:
            self.runDisplay = False
            self.counter = 0
            self.game.currentMenu = self.game.mainMenu

            self.mapArray.clear()

        if self.game.START_KEY and len(self.mapArray) > 0:
            self.runDisplay = False
            self.removeMap(self.chosenMap)
            self.counter = 0
            self.successfullMonit()
            self.game.currentMenu = self.game.mainMenu
            self.mapArray.clear()

        elif self.game.START_KEY and len(self.mapArray) <= 0:
            self.runDisplay = False
            self.game.currentMenu = self.game.loadSaveMenu

    def successfullMonit(self):
        """
        Short once second communicat which display after successfull map delete.
        """
        self.game.display.fill(BLACK)
        self.game.drawText('Map successfully deleted!', 65, midWidth, midHeight,
                           WHITE, self.game.fontName)
        self.blitScreen()
        time.sleep(1)


class LoadSaveMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the module menu, inheriting from the Menu class.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.firstModuleX, self.firstModuleY = midWidth, midHeight
        self.secondModuleX, self.secondModuleY = midWidth, midHeight + 100
        self.thirdModuleX, self.thirdModuleY = midWidth, midHeight + 200
        self.fourthModuleX, self.fourthModuleY = midWidth, midHeight + 300
        self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
        self.state = 'One'
        self.moved = 'No'

    def displayMenu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True
        if self.moved == 'No':
            self.resetPointer()

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('Load game/map from:', 120, midWidth, midHeight - 200, WHITE, self.game.fontName)
            self.game.drawText('Module 2', 80, self.firstModuleX, self.firstModuleY, WHITE, self.game.fontName)
            self.game.drawText('Own maps', 80, self.secondModuleX, self.secondModuleY, WHITE, self.game.fontName)
            self.game.drawText('Own saves', 80, self.thirdModuleX, self.thirdModuleY, WHITE, self.game.fontName)
            self.game.drawText('Del Map', 80, self.fourthModuleX, self.fourthModuleY, WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu. Supports three module selection logic.
        """
        self.movePointer()

        if self.game.BACK_KEY or self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.moved = 'No'

        if self.game.START_KEY:
            self.moved = 'No'
            if self.state == 'One':
                self.game.currentMenu = self.game.resumeSavedGameMenu
                self.game.previousMenu = self.state

            elif self.state == 'Two':
                self.game.currentMenu = self.game.loadMapMenu

            elif self.state == 'Three':
                self.game.currentMenu = self.game.resumeSavedGameMenu
                self.game.previousMenu = self.state

            elif self.state == 'Four':
                self.game.currentMenu = self.game.deleteMapMenu

        self.runDisplay = False

    def resetPointer(self):
        """
        Utility function for reset pointer position after selected action.
        """
        self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
        self.state = 'One'

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            self.moved = 'Yes'
            if self.state == 'One':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'Two'
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset, self.thirdModuleY)
                self.state = 'Three'
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.fourthModuleX + self.offset, self.fourthModuleY)
                self.state = 'Four'
            elif self.state == 'Four':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'One'
        elif self.game.UP_KEY or self.game.W_KEY:
            self.moved = 'Yes'
            if self.state == 'One':
                self.pointerRect.midtop = (self.fourthModuleX + self.offset, self.fourthModuleY)
                self.state = 'Four'
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'One'
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'Two'
            elif self.state == 'Four':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset, self.thirdModuleY)
                self.state = 'Three'


class ResumeSavedGameMenu(Menu):
    def __init__(self, game):
        """
        Sub menu for Module III that allows player to choose his own map.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        Menu.__init__(self, game)
        self.textInfoX, self.textInfoY = midWidth, midHeight - 280
        self.itemMapX, self.itemMapY = midWidth, midHeight - 180
        self.deleteRect = pygame.Rect(midWidth + 450, midHeight + 320, 140, 50)
        self.offset = -100
        self.pointerRect = pygame.Rect(0, 0, 20, 20)
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + 10)
        self.counter = 0
        self.storekeeperImg = pygame.transform.scale(STOREKEEPER_IMG, (40, 40))
        self.mapArray = []
        self.chosenMap = ''

    def displayMenu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True
        maps = os.listdir(SAVES_DIR)

        amount = 0

        self.cleanMaps(maps, self.game.previousMenu)
        self.game.previousMenu = ''
        self.resetPointer()

        if len(self.mapArray) > 0:
            self.chosenMap = self.mapArray[0]
            while self.runDisplay:
                self.game.resetKeys()
                self.game.checkEvents()
                self.checkInput()

                self.game.display.fill(BLACK)
                self.game.drawText('CHOOSE MAP', 65, self.textInfoX, self.textInfoY,
                                   WHITE, self.game.fontName)

                for row in range(len(self.mapArray)):
                    if row < 12:
                        board = self.prepareSaveName(self.mapArray[row])
                        self.game.drawText(str(board), 28, self.itemMapX, self.itemMapY + (row * 45),
                                           WHITE, self.game.fontName)

                self.drawPointer()
                self.blitScreen()
        else:
            while self.runDisplay:
                self.game.resetKeys()
                self.game.checkEvents()
                self.checkInput()

                self.game.display.fill(BLACK)
                self.game.drawText('YOU HAVE NOT CREATED ANY SAVES', 65, midWidth, midHeight,
                                   WHITE, self.game.fontName)

                self.blitScreen()

    def resetPointer(self):
        """
        Utility function for reset pointer position after selected action.
        """
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + 10)
        self.chosenMap = ''

    def prepareSaveName(self, filename):
        """
        Utility function for preparing player save game for nice format.

        :param filename:
            Name of the file which contains save.
        :type filename: str, required

        :return:
            Nice looking save game name.
        :rtype: str
        """
        playerName = filename[:filename.find('_')]
        hours = filename[len(playerName) + 1:]

        hour = hours[:8]
        date = hours[9:19]

        hour = hour.replace('_', ':')
        date = date.replace('_', '/')

        result = ''.join((playerName, '        ', hour, '    ', date))

        return result

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            self.counter += 1

            if self.counter > len(self.mapArray) - 1 or self.counter > 11:
                self.counter = 0

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + (self.counter * 45))
            self.chosenMap = self.mapArray[self.counter]

        elif self.game.UP_KEY or self.game.W_KEY:
            self.counter -= 1

            if self.counter < 0:
                self.counter = len(self.mapArray) - 1

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + self.counter * 45)
            self.chosenMap = self.mapArray[self.counter]

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.ESC_PRESSED:
            self.runDisplay = False
            self.mapArray.clear()
            self.game.currentMenu = self.game.mainMenu

        if self.game.START_KEY and len(self.mapArray) > 0:
            self.runDisplay = False
            self.game.logicState = True
            self.game.restoreDetails = logic.loadSave(self.chosenMap[:len(self.chosenMap) - 4])

            self.mapArray.clear()

            if self.game.restoreDetails['flag'] == MODULE_II:
                self.game.gameLevel = self.game.restoreDetails['lvlName']

                logic.startTheGame(self.game.window, self.chosenMap,
                                   self.game, self.game.gamePoints, RESTORE)

                if self.game.gameLevel > self.game.restoreDetails['lvlName']:
                    while self.game.gameLevel <= 20 and self.game.START_KEY:
                        self.game.currentLevel = self.game.gameLevel
                        boardName = str(self.game.currentLevel) + '.txt'

                        logic.startTheGame(self.game.window, boardName, self.game,
                                           self.game.gamePoints, MODULE_II)

                        self.game.logicState = True

            elif self.game.restoreDetails['flag'] == MODULE_III:
                logic.startTheGame(self.game.window, self.chosenMap,
                                   self.game, self.game.gamePoints, RESTORE)

            self.game.restoreDetails.clear()

        elif self.game.START_KEY and len(self.mapArray) <= 0:
            self.runDisplay = False
            self.game.currentMenu = self.game.loadSaveMenu

            self.mapArray.clear()

    def prepareSaveName(self, filename):
        """
        Utility function for preparing player save game for nice format.

        :param filename:
            Name of the file which contains save.
        :type filename: str, required

        :return:
            Nice looking save game name.
        :rtype: str
        """
        playerName = filename[:filename.find('_')]
        hours = filename[len(playerName) + 1:]

        hour = hours[:8]
        date = hours[9:19]

        hour = hour.replace('_', ':')
        date = date.replace('_', '/')

        result = ''.join((playerName, '        ', hour, '    ', date))

        return result

    def cleanMaps(self, maps, previousState):
        """
        Method for choosing map based on before selected menu.

        :param maps:
            List of game saves in folder SAVES_DIR.
        :type maps: list, required
        :param previousState:
            Flag that allows to discriminate module II and III saved games.
        :type previousState: str, required
        """
        for file in maps:
            if file.find('.bak') > -1 and \
                    re.search(rf'\b{self.game.playerName}(_)(.*)\b', file):
                if re.search(rf'\b(.*)(_){previousState}\b', file):
                    self.mapArray.append(file)
