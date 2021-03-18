import json
import os
import time
from pygame.locals import *
from src.modules import logic
from random import randrange
from .player import *


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
        self.game.display.blit(self.storekeeperImg, (self.pointerRect.x - 200, self.pointerRect.y - 30))

    def blitScreen(self):
        """
        Method that updates the screen, resets the keys and blits the display on the window.
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
        self.levelMenuX, self.levelMenuY = midWidth, midHeight + 30
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

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('SOKOBAN', 130, self.logoMenuX, self.logoMenuY, self.game.WHITE, self.game.fontTitle)
            self.game.drawText('Start Game', 70, self.startMenuX, self.startMenuY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Load Game', 70, self.levelMenuX, self.levelMenuY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Instructions', 70, self.instructionsMenuX, self.instructionsMenuY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Ranking', 70, self.rankingMenuX, self.rankingMenuY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Credits', 70, self.creditsMenuX, self.creditsMenuY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Quit', 70, self.quitMenuX, self.quitMenuY, self.game.WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            if self.state == 'Start':
                self.pointerRect.midtop = (self.levelMenuX + self.offset, self.levelMenuY)
                self.state = 'Level'
            elif self.state == 'Level':
                self.pointerRect.midtop = (self.instructionsMenuX + self.offset, self.instructionsMenuY)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.pointerRect.midtop = (self.rankingMenuX + self.offset, self.rankingMenuY)
                self.state = 'Ranking'
            elif self.state == 'Ranking':
                self.pointerRect.midtop = (self.creditsMenuX + self.offset, self.creditsMenuY)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.pointerRect.midtop = (self.quitMenuX + self.offset, self.quitMenuY)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.pointerRect.midtop = (self.startMenuX + self.offset, self.startMenuY)
                self.state = 'Start'
        elif self.game.UP_KEY or self.game.W_KEY:
            if self.state == 'Start':
                self.pointerRect.midtop = (self.quitMenuX + self.offset, self.quitMenuY)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.pointerRect.midtop = (self.creditsMenuX + self.offset, self.creditsMenuY)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.pointerRect.midtop = (self.rankingMenuX + self.offset, self.rankingMenuY)
                self.state = 'Ranking'
            elif self.state == 'Ranking':
                self.pointerRect.midtop = (self.instructionsMenuX + self.offset, self.instructionsMenuY)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.pointerRect.midtop = (self.levelMenuX + self.offset, self.levelMenuY)
                self.state = 'Level'
            elif self.state == 'Level':
                self.pointerRect.midtop = (self.startMenuX + self.offset, self.startMenuY)
                self.state = 'Start'

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu depending on whether player has given its nickname.
        """
        self.movePointer()

        if self.game.START_KEY:
            if self.state == 'Start' and len(self.game.playerName) == 0:
                self.game.currentMenu = self.game.inputMenu
            elif self.state == 'Start' and len(self.game.playerName) > 0:
                self.game.START_KEY = False
                self.game.currentMenu = self.game.levelMenu
            # elif self.state == 'Level' and len(self.game.playerName) == 0:
            #     self.game.currentMenu = self.game.inputMenu
            elif self.state == 'Level':# and len(self.game.playerName) > 0:
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


class LevelMenu(Menu):
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
        self.level = 1
        self.state = 'One'
        self.visited = False

    def displayMenu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('Choose module: ', 120, midWidth, midHeight - 200, self.game.WHITE, self.game.fontName)
            self.game.drawText('Module 1', 80, self.firstModuleX, self.firstModuleY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Module 2', 80, self.secondModuleX, self.secondModuleY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Module 3', 80, self.thirdModuleX, self.thirdModuleY, self.game.WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu. Supports three module selection logic.
        """
        self.movePointer()

        if self.game.BACK_KEY or self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False

        if self.game.START_KEY:
            if self.state == 'One':
                self.runDisplay = False
                self.game.currentMenu = self.game.diffMenu

            elif self.state == 'Two':
                self.runDisplay = False
                self.game.logicState = True

                while self.game.gameLevel <= 20 and self.game.START_KEY:
                    currLvl = str(self.game.gameLevel)

                    logic.startTheGame(self.game.window, currLvl + ".txt",
                                       self.game, self.game.gamePoints, MODULE_II)

                    self.game.logicState = True

            elif self.state == 'Three':
                self.runDisplay = False
                self.game.currentMenu = self.game.widthHeightMenu
            # else:
            #     self.game.currentMenu = self.game.mainMenu

            self.runDisplay = False

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            if self.state == 'One':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'Two'
                self.visited = True
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset, self.thirdModuleY)
                self.state = 'Three'
                self.visited = True
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'One'
                self.visited = True
        elif self.game.UP_KEY or self.game.W_KEY:
            if self.state == 'One':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset, self.thirdModuleY)
                self.state = 'Three'
                self.visited = True
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'One'
                self.visited = True
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'Two'
                self.visited = True


class CreditsMenu(Menu):
    def __init__(self, game):
        """
        Class which represents the credits menu, inheriting from the Menu class. Shows the info about the game developers.

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
        Method that displays the menu. It prints 7 buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('THE GAME HAS BEEN WRITTEN BY', 85, self.creditsTitleX, self.creditsTitleY, self.game.WHITE, self.game.fontName)
            self.game.drawText('PIOTR BATOR', 70, self.firstAuthorX, self.firstAuthorY, self.game.WHITE, self.game.fontName)
            self.game.drawText('GABRIEL BRZOSKWINIA', 70, self.secondAuthorX, self.secondAuthorY, self.game.WHITE, self.game.fontName)
            self.game.drawText('AS A PART OF', 60, self.partOneX, self.partOneY, self.game.WHITE, self.game.fontName)
            self.game.drawText('THE MOTOROLA SCIENCE CUP', 60, self.partTwoX, self.partTwoY, self.game.RED, self.game.fontName)
            self.game.drawText('COMPETITION TASKS', 60, self.partThreeX, self.partThreeY, self.game.WHITE, self.game.fontName)
            self.game.drawText('2021 © ALL RIGHTS RESERVED', 30, self.copyrightX, self.copyrightY, self.game.WHITE, self.game.fontName)

            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if self.game.BACK_KEY:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False
        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False
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
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.display.blit(self.image, (self.instructionsTextX - 250, self.instructionsTextY + 150))
            self.game.drawText('USE', 55, self.instructionsTextX - 450, self.instructionsTextY, self.game.WHITE, self.game.fontName)
            self.game.drawText('WSAD', 55, self.instructionsTextX - 340, self.instructionsTextY, self.game.RED, self.game.fontName)
            self.game.drawText('IN ORDER TO MOVE YOUR STOREKEEPER', 55, self.instructionsTextX + 150, self.instructionsTextY, self.game.WHITE, self.game.fontName)

            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if self.game.START_KEY:
            self.game.currentMenu = self.game.legendMenu
            self.runDisplay = False
        if self.game.BACK_KEY or self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
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
            self.game.drawText('RULES', 100, self.legendTextX, self.legendTextY, self.game.WHITE, self.game.fontName)
            self.game.drawText('IT IS A LOGICAL GAME WHOSE AIM IS TO MOVE', 45, self.legendTextX, self.legendTextY + 150, self.game.WHITE, self.game.fontName)
            self.game.drawText('AND CORRECTLY POSITION THE', 45, self.legendTextX - 180, self.legendTextY + 220, self.game.WHITE, self.game.fontName)
            self.game.drawText('BOXES', 45, self.legendTextX + 150, self.legendTextY + 220, self.game.RED, self.game.fontName)
            self.game.drawText('IN A WAREHOUSE.', 45, self.legendTextX + 365, self.legendTextY + 220, self.game.WHITE, self.game.fontName)
            self.game.drawText('YOU WILL PLAY AS THE', 45, self.legendTextX - 300, self.legendTextY + 290, self.game.WHITE, self.game.fontName)
            self.game.drawText('WAREHOUSE KEEPER', 45, self.legendTextX + 90, self.legendTextY + 290, self.game.RED, self.game.fontName)
            self.game.drawText('AND TRY TO COPE', 45, self.legendTextX + 430, self.legendTextY + 290, self.game.WHITE, self.game.fontName)
            self.game.drawText('WITH THE CHALLENGE, FACING', 45, self.legendTextX - 300, self.legendTextY + 360, self.game.WHITE, self.game.fontName)
            self.game.drawText('20 MAPS', 45, self.legendTextX + 50, self.legendTextY + 360, self.game.RED, self.game.fontName)
            self.game.drawText('OF VARYING DIFFICULTY.', 45, self.legendTextX + 350, self.legendTextY + 360, self.game.WHITE, self.game.fontName)
            self.game.drawText('WE WISH YOU GOOD LUCK!', 45, self.legendTextX, self.legendTextY + 500, self.game.WHITE, self.game.fontName)

            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        if self.game.BACK_KEY:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False
        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False
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

    def displayMenu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)

            self.game.drawText('SELECT YOUR DIFFICULTY', 85, self.diffTitleX, self.diffTitleY, self.game.WHITE, self.game.fontName)
            self.game.drawText('EASY', 80, self.easyX, self.easyY, self.game.WHITE, self.game.fontName)
            self.game.drawText('MEDIUM', 80, self.mediumX, self.mediumY, self.game.WHITE, self.game.fontName)
            self.game.drawText('HARD', 80, self.hardX, self.hardY, self.game.WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.BACK_KEY:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False
        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False
        if self.game.START_KEY:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        Depending on the chosen difficulty, the player draws a map from three fields.
        """
        if self.game.START_KEY:
            if self.state == 'Easy':
                self.game.logicState = True
                self.game.currentLevel = str(randrange(1, 20))
                logic.startTheGame(self.game.window, self.game.currentLevel + ".txt", self.game, self.game.gamePoints, MODULE_I)

                self.runDisplay = False

            elif self.state == 'Medium':
                self.game.logicState = True
                self.game.currentLevel = str(randrange(21, 40))
                self.runDisplay = False
                logic.startTheGame(self.game.window, self.game.currentLevel + ".txt", self.game, self.game.gamePoints, MODULE_I)

            elif self.state == 'Hard':
                self.game.logicState = True
                self.game.currentLevel = str(randrange(41, 60))
                self.runDisplay = False
                logic.startTheGame(self.game.window, self.game.currentLevel + ".txt", self.game, self.game.gamePoints, MODULE_I)

        if self.game.DOWN_KEY or self.game.S_KEY:
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
            if self.state == 'Easy':
                self.pointerRect.midtop = (self.hardX + self.offset, self.hardY)
                self.state = 'Hard'
            elif self.state == 'Medium':
                self.pointerRect.midtop = (self.easyX + self.offset, self.easyY)
                self.state = 'Easy'
            elif self.state == 'Hard':
                self.pointerRect.midtop = (self.mediumX + self.offset, self.mediumY)
                self.state = 'Medium'


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
            self.game.currentMenu = self.game.levelMenu
            self.game.currentMenu.displayMenu()

        elif self.game.ESC_PRESSED or self.game.BACK_KEY:
            self.runDisplay = False
            self.game.playerName = ''
            self.game.running = True
            self.game.currentMenu = self.game.mainMenu
            self.game.currentMenu.displayMenu()

    def inputName(self):
        """
        Function for handling player writing his nickname.
        """
        self.game.running = False

        event = pygame.event.poll()
        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)  # Returns string id of pressed key.

            if len(key) == 1:  # This covers all letters and numbers not on numpad.
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

        self.game.drawText(self.game.playerName, 60, self.inputNameX, self.inputNameY + 350, self.game.RED,
                            self.game.fontName)
        self.game.drawText('Chars used: ' + str(len(self.game.playerName)), 30, self.inputNameX, self.inputNameY + 600,
                            self.game.WHITE, self.game.fontName)

    def displayMenu(self):
        """
        Method that displays the menu. It prints 2 buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.display.fill(BLACK)
            self.game.drawText('TYPE IN YOUR NICKNAME [15]', 95, self.inputNameX, self.inputNameY + 50, self.game.WHITE,
                                self.game.fontName)
            self.game.drawText('AND PRESS ENTER TO CONFIRM', 70, self.inputNameX, self.inputNameY + 150, self.game.WHITE,
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
            self.game.drawText('RANKING', 90, self.headerX, self.headerY, self.game.WHITE, self.game.fontName)
            self.game.drawText('NAME', 60, self.headerX - 300, self.headerY + 100, self.game.WHITE, self.game.fontName)
            self.game.drawText('POINTS', 60, self.headerX + 300, self.headerY + 100, self.game.WHITE, self.game.fontName)

            def getScore(table):
                return table.get('userScore')

            with open('scoreFile.txt', 'r') as scoreFile:
                table = [json.loads(line) for line in scoreFile]
                counter = 1

                table.sort(key=getScore, reverse = True)

                for row in table:
                    name = table[counter - 1]['userNameVar']
                    points = table[counter - 1]['userScore']
                    if counter <= 5:
                        self.game.drawText(str(counter) + '. ' + str(name), 50, self.headerX - 300, self.itemY + (counter * 60), self.game.WHITE, self.game.fontName)
                        self.game.drawText(str(points), 50, self.headerX + 300, self.itemY + (counter * 60), self.game.RED, self.game.fontName)
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

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('DO YOU WANT TO QUIT AND SAVE YOUR SCORE?', 65, midWidth, midHeight - 300,
                                self.game.WHITE,
                                self.game.fontName)
            self.game.drawText('YES', 60, self.firstModuleX, self.firstModuleY,
                                self.game.WHITE,
                                self.game.fontName)
            self.game.drawText('NO', 60, self.secondModuleX, self.secondModuleY,
                                self.game.WHITE,
                                self.game.fontName)

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

                currLvl = str(self.game.currentLevel) + '.txt'

                logic.saveBoard(self.game.currentPlayerState['width'], self.game.currentPlayerState['height'],
                                self.game.currentPlayerState['sprites'], self.game.currentPlayerState['time'],
                                self.game.playerName, currLvl, self.game.gamePoints)

                if self.game.gameLevel > 1:
                    self.game.gameLevel = 1


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
            if 0 < int(self.passedWidth) <= 30 and 0 < int(self.passedHeight) <= 20 and 0 < len(self.game.passedMapName) <= 15:
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
                    if (event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9) and len(self.passedWidth)  < 2:
                        self.passedWidth += event.unicode

            elif self.buttonHActive:
                if key == 'backspace':
                    self.passedHeight = self.passedHeight[:-1]
                elif key == 'return':
                    if len(self.passedHeight) > 0 and len(self.passedWidth) > 0:
                        self.game.START_KEY = True
                else:
                    if (event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9) and len(self.passedHeight)  < 2:
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
                           self.game.WHITE, self.game.fontName)
        self.game.drawText(self.passedHeight, 50, self.heightX + 150, self.heightY,
                            self.game.WHITE,
                            self.game.fontName)
        self.game.drawText(self.game.passedMapName, 40, self.nameX + 325, self.nameY,
                            self.game.WHITE,
                            self.game.fontName)

    def displayMenu(self):
        """
        Method that displays the menu. It prints buttons thanks to the drawText() method.
        It also blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.display.fill(BLACK)
            self.game.drawText('ENTER YOUR MAP DIMENSIONS', 65, self.textInfoX, self.textInfoY,
                               self.game.WHITE, self.game.fontName)
            self.game.drawText('MAX: 30 x 20', 35, self.textInfoX, self.textInfoY + 50,
                               self.game.RED, self.game.fontName)
            self.game.drawText('WIDTH: ', 60, self.widthX, self.widthY,self.game.WHITE,
                               self.game.fontName)
            self.game.drawText('HEIGHT: ', 60, self.heightX, self.heightY,
                               self.game.WHITE, self.game.fontName)

            self.game.drawText('NAME: ', 60, self.nameX, self.nameY,
                                self.game.WHITE,
                                self.game.fontName)


            self.inputHandle()
            self.checkInput()
            self.blitScreen()


class LoadMapMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        """
        Sub menu for Module III that allows player to choose his own map.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        self.textInfoX, self.textInfoY = midWidth, midHeight - 280
        self.itemMapX, self.itemMapY = midWidth, midHeight - 200
        self.chosenMap = ''
        self.deleteRect = pygame.Rect(midWidth + 450, midHeight + 320, 140, 50)
        self.offset = -100
        self.pointerRect = pygame.Rect(0, 0, 20, 20)
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY)
        self.counter = 0
        self.storekeeperImg = pygame.transform.scale(STOREKEEPER_IMG, (40, 40))

    def displayMenu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True

        self.mapArray = os.listdir('./src/boards/own/')
        self.chosenMap = self.mapArray[0]

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('CHOOSE MAP', 65, self.textInfoX, self.textInfoY,
                                self.game.WHITE,
                                self.game.fontName)

            for row in range(len(self.mapArray)):
                map = self.mapArray[row]
                self.game.drawText(str(map), 20, self.itemMapX, self.itemMapY + (row * 40), self.game.WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            self.counter += 1

            if self.counter > len(self.mapArray) - 1:
                self.counter = 0

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + (self.counter * 40))
            self.chosenMap = self.mapArray[self.counter]

            print(self.chosenMap)
        elif self.game.UP_KEY or self.game.W_KEY:
            self.counter -= 1

            if self.counter < 0:
                self.counter = len(self.mapArray) - 1

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + self.counter * 40)
            self.chosenMap = self.mapArray[self.counter]

            print(self.chosenMap)

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            # self.game.running = True
            self.runDisplay = False

        if self.game.START_KEY:
            self.runDisplay = False
            self.game.logicState = True

            logic.startTheGame(self.game.window, self.chosenMap,
                               self.game, self.game.gamePoints, MODULE_III)


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
        self.itemMapX, self.itemMapY = midWidth, midHeight - 200
        self.chosenMap = ''
        self.offset = -100
        self.pointerRect = pygame.Rect(0, 0, 20, 20)
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY)
        self.counter = 0

    def displayMenu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True

        self.mapArray = os.listdir('./src/boards/own/')
        self.chosenMap = self.mapArray[0]

        while self.runDisplay:
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('DELETE YOUR MAP', 65, self.textInfoX, self.textInfoY,
                                self.game.WHITE,
                                self.game.fontName)

            for row in range(len(self.mapArray)):
                map = self.mapArray[row]
                self.game.drawText(str(map), 20, self.itemMapX, self.itemMapY + (row * 40), self.game.WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def removeMap(self, mapID):
        """
        Function for module III which allows player to delete his own map.

        :param playerName:
            Map creator nick name.
        :type playerName: str, required
        :param mapID:
            ID of created map.
        :type mapID: int, required
        """
        if os.path.isfile('./src/boards/own/' + str(mapID)):
            os.remove('./src/boards/own/' + mapID)
            print(f'Map deleted successfully.')
        #     self.runDisplay = False
        #     self.game.currentMenu = self.game.mainMenu
        #     self.game.currentMenu.displayMenu
        # else:
        #     print(f'File not exist.')
        #     self.runDisplay = False
        #     self.game.currentMenu = self.game.mainMenu
        #     self.game.currentMenu.displayMenu

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            self.counter += 1

            if self.counter > len(self.mapArray) - 1:
                self.counter = 0

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + (self.counter * 40))
            self.chosenMap = self.mapArray[self.counter]

            print(self.chosenMap)
        elif self.game.UP_KEY or self.game.W_KEY:
            self.counter -= 1

            if self.counter < 0:
                self.counter = len(self.mapArray) - 1

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + self.counter * 40)
            self.chosenMap = self.mapArray[self.counter]

            print(self.chosenMap)

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.ESC_PRESSED:
            self.runDisplay = False
            self.game.currentMenu = self.game.mainMenu
            self.counter = 0

        if self.game.START_KEY:
            self.removeMap(self.chosenMap)
            self.successfullMonit()
            self.runDisplay = False
            self.counter = 0
            self.game.currentMenu = self.game.mainMenu

    def successfullMonit(self):
        self.game.display.fill(BLACK)
        self.game.drawText('Map successfully deleted!', 65, midWidth, midHeight, WHITE,
                           self.game.fontName)
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
        self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
        self.state = 'One'
        self.visited = False

    def displayMenu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('Load game/map from:', 120, midWidth, midHeight - 200, self.game.WHITE, self.game.fontName)
            self.game.drawText('Module 2', 80, self.firstModuleX, self.firstModuleY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Module 3', 80, self.secondModuleX, self.secondModuleY, self.game.WHITE, self.game.fontName)
            self.game.drawText('Del Map', 80, self.thirdModuleX, self.thirdModuleY, self.game.WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu. Supports three module selection logic.
        """
        self.movePointer()

        if self.game.BACK_KEY or self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            self.runDisplay = False

        if self.game.START_KEY:
            if self.state == 'One':
                self.runDisplay = False
                self.game.currentMenu = self.game.resumeSavedGameMenu

            elif self.state == 'Two':
                self.runDisplay = False
                self.game.currentMenu = self.game.loadMapMenu

            elif self.state == 'Three':
                self.runDisplay = False
                self.game.currentMenu = self.game.deleteMapMenu

            self.runDisplay = False

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            if self.state == 'One':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'Two'
                self.visited = True
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset, self.thirdModuleY)
                self.state = 'Three'
                self.visited = True
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'One'
                self.visited = True
        elif self.game.UP_KEY or self.game.W_KEY:
            if self.state == 'One':
                self.pointerRect.midtop = (self.thirdModuleX + self.offset, self.thirdModuleY)
                self.state = 'Three'
                self.visited = True
            elif self.state == 'Two':
                self.pointerRect.midtop = (self.firstModuleX + self.offset, self.firstModuleY)
                self.state = 'One'
                self.visited = True
            elif self.state == 'Three':
                self.pointerRect.midtop = (self.secondModuleX + self.offset, self.secondModuleY)
                self.state = 'Two'
                self.visited = True


class ResumeSavedGameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        """
        Sub menu for Module III that allows player to choose his own map.

        :param game:
            Game class that allows connection between game logic and menu.
        :type game: game.Game, required
        """
        self.textInfoX, self.textInfoY = midWidth, midHeight - 280
        self.itemMapX, self.itemMapY = midWidth, midHeight - 200
        self.chosenMap = ''
        self.deleteRect = pygame.Rect(midWidth + 450, midHeight + 320, 140, 50)
        self.offset = -100
        self.pointerRect = pygame.Rect(0, 0, 20, 20)
        self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY)
        self.counter = 0
        self.storekeeperImg = pygame.transform.scale(STOREKEEPER_IMG, (40, 40))
        self.mapArray = []

    def displayMenu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the drawText() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.runDisplay = True
        maps = os.listdir('src/saves/')
        print(maps)
        for file in maps:
            print(file)
            if file.find('.bak') > -1:
                self.mapArray.append(file)

        self.chosenMap = self.mapArray[0]

        while self.runDisplay:
            self.game.resetKeys()
            self.game.checkEvents()
            self.checkInput()

            self.game.display.fill(BLACK)
            self.game.drawText('CHOOSE MAP', 65, self.textInfoX, self.textInfoY,
                                self.game.WHITE,
                                self.game.fontName)

            for row in range(len(self.mapArray)):
                map = self.mapArray[row]
                self.game.drawText(str(map), 20, self.itemMapX, self.itemMapY + (row * 40), self.game.WHITE, self.game.fontName)

            self.drawPointer()
            self.blitScreen()

    def movePointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY or self.game.S_KEY:
            self.counter += 1

            if self.counter > len(self.mapArray) - 1:
                self.counter = 0

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + (self.counter * 40))
            self.chosenMap = self.mapArray[self.counter]

            print(self.chosenMap)
        elif self.game.UP_KEY or self.game.W_KEY:
            self.counter -= 1

            if self.counter < 0:
                self.counter = len(self.mapArray) - 1

            self.pointerRect.midtop = (self.itemMapX + self.offset, self.itemMapY + self.counter * 40)
            self.chosenMap = self.mapArray[self.counter]

            print(self.chosenMap)

    def checkInput(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.movePointer()

        if self.game.ESC_PRESSED:
            self.game.currentMenu = self.game.mainMenu
            # self.game.running = True
            self.runDisplay = False

        if self.game.START_KEY:
            self.runDisplay = False
            self.game.logicState = True

            self.game.restoreDetails = logic.loadSave(self.chosenMap[:len(self.chosenMap) - 4])

            print(f'Before start')
            logic.startTheGame(self.game.window, self.chosenMap,
                               self.game, self.game.gamePoints, 'RESTORE')
