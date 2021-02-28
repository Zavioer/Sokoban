import pygame
from src.modules import logic
from random import randrange


class Menu:
    """
    Class which represents the menu.
    """
    def __init__(self, game):
        """
        :attributes
            run_display: bool
                State of checking if the displays can be printed.
            pointer_rect: pygame.Rect
                Pygame Rect class of pointer instance.
        :param
        game: class, required
            Game class
        """
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.pointer_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_pointer(self):
        """
        Method that draws the pointer on the display.
        """
        self.game.draw_text('*', 60, self.pointer_rect.x - 150, self.pointer_rect.y, self.game.WHITE, self.game.font_name)

    def blit_screen(self):
        """
        Method that updates the screen, resets the keys and blits the display on the window.
        """
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    """
    Class which represents the main menu, inheriting from the Menu class.
    """
    def __init__(self, game):
        Menu.__init__(self, game)
        """
        :attributes
        logox, startx, levelx, instructionsx, creditsx, quitx - Buttons initial x coordinates.
        logoy, starty, levely, instructionsy, creditsy, quity - Buttons initial y coordinates.
        :param
        game: class, required
            Game class
        """
        self.state = "Start"
        self.logox, self.logoy = self.mid_w, self.mid_h - 230
        self.startx, self.starty = self.mid_w, self.mid_h - 40
        self.levelx, self.levely = self.mid_w, self.mid_h + 40
        self.instructionsx, self.instructionsy = self.mid_w, self.mid_h + 120
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 200
        self.quitx, self.quity = self.mid_w, self.mid_h + 280
        self.pointer_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        """
        Method that displays the menu. It prints 6 buttons thanks to the draw_text() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("SOKOBAN", 130, self.logox, self.logoy, self.game.WHITE, self.game.font_title)
            self.game.draw_text("Start Game", 70, self.startx, self.starty, self.game.WHITE, self.game.font_name)
            self.game.draw_text("Load Level", 70, self.levelx, self.levely, self.game.WHITE, self.game.font_name)
            self.game.draw_text("Instructions", 70, self.instructionsx, self.instructionsy, self.game.WHITE, self.game.font_name)
            self.game.draw_text("Credits", 70, self.creditsx, self.creditsy, self.game.WHITE, self.game.font_name)
            self.game.draw_text("Quit", 70, self.quitx, self.quity, self.game.WHITE, self.game.font_name)
            self.draw_pointer()
            self.blit_screen()

    def move_pointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.pointer_rect.midtop = (self.levelx + self.offset, self.levely)
                self.state = 'Level'
            elif self.state == 'Level':
                self.pointer_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.pointer_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.pointer_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.pointer_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.pointer_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.pointer_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.pointer_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.pointer_rect.midtop = (self.levelx + self.offset, self.levely)
                self.state = 'Level'
            elif self.state == 'Level':
                self.pointer_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.move_pointer()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.level
            elif self.state == 'Level':
                self.game.curr_menu = self.game.level
            elif self.state == 'Instructions':
                self.game.curr_menu = self.game.instructions
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                pass
            self.run_display = False


class LevelMenu(Menu):
    """
    Class which represents the module menu, inheriting from the Menu class.
    """
    def __init__(self, game):
        """
        :attributes
        firstx, secondx, thirdx - Buttons initial x coordinates.
        firsty, secondy, thirdy - Buttons initial y coordinates.
        level - string, required
            Game's module choice. [default = '']
        state - string, required
            pointer state variable [default = 'One']

        :param
        game: class, required
            Game class
        """
        Menu.__init__(self, game)
        self.state = 'One'
        self.firstx, self.firsty = self.mid_w, self.mid_h
        self.secondx, self.secondy = self.mid_w, self.mid_h + 100
        self.thirdx, self.thirdy = self.mid_w, self.mid_h + 200
        self.pointer_rect.midtop = (self.firstx + self.offset, self.firsty)
        self.level = 1

    def display_menu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the draw_text() method.
        It also draws the pointer and blits the screen every single frame.
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Choose module: ", 120, self.mid_w, self.mid_h - 200, self.game.WHITE, self.game.font_name)
            self.game.draw_text("Module 1", 80, self.firstx, self.firsty, self.game.WHITE, self.game.font_name)
            self.game.draw_text("Module 2", 80, self.secondx, self.secondy, self.game.WHITE, self.game.font_name)
            self.game.draw_text("Module 3", 80, self.thirdx, self.thirdy, self.game.WHITE, self.game.font_name)
            self.draw_pointer()
            self.blit_screen()

    def check_input(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.move_pointer()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.ESC_PRESSED:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.START_KEY:
            if self.state == 'One':
                self.game.curr_menu = self.game.diff_menu
            elif self.state == 'Two':
                logic.start_the_game(self.game.window, str(self.game.gameLevel) + ".txt", self.game)
            elif self.state == 'Three':
                # logic.create_map()
                pass
            else:
                self.game.curr_menu = self.game.main_menu
            self.run_display = False

    def move_pointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.DOWN_KEY:
            if self.state == 'One':
                self.pointer_rect.midtop = (self.secondx + self.offset, self.secondy)
                self.state = 'Two'

            elif self.state == 'Two':
                self.pointer_rect.midtop = (self.thirdx + self.offset, self.thirdy)
                self.state = 'Three'

            elif self.state == 'Three':
                self.pointer_rect.midtop = (self.firstx + self.offset, self.firsty)
                self.state = 'One'

        elif self.game.UP_KEY:
            if self.state == 'One':
                self.pointer_rect.midtop = (self.thirdx + self.offset, self.thirdy)
                self.state = 'Three'

            if self.state == 'Two':
                self.pointer_rect.midtop = (self.firstx + self.offset, self.firsty)
                self.state = 'One'

            if self.state == 'Three':
                self.pointer_rect.midtop = (self.secondx + self.offset, self.secondy)
                self.state = 'Two'


class CreditsMenu(Menu):
    """
    Class which represents the credits menu, inheriting from the Menu class.
    """
    def __init__(self, game):
        """
        :attributes
        titlex, fauthorx, sauthorx, partx, tournamentx, tasksx, copyrightx - Buttons initial x coordinates.
        titley, fauthory, sauthory, party, tournamenty, tasksy, copyrighty - Buttons initial y coordinates.

        :param
        game: class, required
            Game class
        """
        Menu.__init__(self, game)
        self.titlex, self.titley = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 280
        self.fauthorx, self.fauthory = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150
        self.sauthorx, self.sauthory = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 70
        self.partx, self.party = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60
        self.tournamentx, self.tournamenty = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 140
        self.tasksx, self.tasksy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 220
        self.copyrightx, self.copyrighty = self.game.DISPLAY_W - 175, self.game.DISPLAY_H - 15

    def display_menu(self):
        """
        Method that displays the menu. It prints 7 buttons thanks to the draw_text() method.
        It also blits the screen every single frame.
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC_PRESSED:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('THE GAME HAS BEEN WRITTEN BY', 85, self.titlex, self.titley, self.game.WHITE, self.game.font_name)
            self.game.draw_text('PIOTR BATOR', 70, self.fauthorx, self.fauthory, self.game.WHITE, self.game.font_name)
            self.game.draw_text('GABRIEL BRZOSKWINIA', 70, self.sauthorx, self.sauthory, self.game.WHITE, self.game.font_name)
            self.game.draw_text('AS A PART OF', 60, self.partx, self.party, self.game.WHITE, self.game.font_name)
            self.game.draw_text('THE MOTOROLA SCIENCE CUP', 60, self.tournamentx, self.tournamenty, self.game.RED, self.game.font_name)
            self.game.draw_text('COMPETITION TASKS', 60, self.tasksx, self.tasksy, self.game.WHITE, self.game.font_name)
            self.game.draw_text('2021 © ALL RIGHTS RESERVED', 30, self.copyrightx, self.copyrighty, self.game.WHITE, self.game.font_name)

            self.blit_screen()


class InstructionsMenu(Menu):
    """
    Class which represents the instructions menu, inheriting from the Menu class.
    """
    def __init__(self, game):
        """
        :attributes
        textx - Buttons initial x coordinates.
        texty - Buttons initial y coordinates.

        :param
        game: class, required
            Game class
        """
        Menu.__init__(self, game)
        self.textx, self.texty = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 280

    def display_menu(self):
        """
        Method that displays the menu. It prints 3 buttons thanks to the draw_text() method.
        It also blits the screen every single frame.
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY:
                self.game.curr_menu = self.game.legend_menu
                self.run_display = False
            if self.game.BACK_KEY or self.game.ESC_PRESSED:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('USE', 55, self.textx - 450, self.texty, self.game.WHITE, self.game.font_name)
            self.game.draw_text('WSAD', 55, self.textx - 340, self.texty, self.game.RED, self.game.font_name)
            self.game.draw_text('IN ORDER TO MOVE YOUR STOREKEEPER', 55, self.textx + 150, self.texty, self.game.WHITE, self.game.font_name)

            self.blit_screen()


class LegendMenu(Menu):
    """
    Class which represents the legend menu, inheriting from the Menu class.
    """
    def __init__(self, game):
        """
        :attributes
        textx, - Buttons initial x coordinates.
        texty, - Buttons initial y coordinates.

        :param
        game: class, required
            Game class
        """
        Menu.__init__(self, game)
        self.textx, self.texty = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 280

    def display_menu(self):
        """
        Method that displays the menu. It prints 11 buttons thanks to the draw_text() method.
        It also blits the screen every single frame.
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC_PRESSED:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('IT IS A LOGICAL GAME WHOSE AIM IS TO MOVE', 45, self.textx, self.texty + 150, self.game.WHITE, self.game.font_name)
            self.game.draw_text('AND CORRECTLY POSITION THE', 45, self.textx - 180, self.texty + 220, self.game.WHITE, self.game.font_name)
            self.game.draw_text('BOXES', 45, self.textx + 150 , self.texty + 220, self.game.RED, self.game.font_name)
            self.game.draw_text('IN A WAREHOUSE.', 45, self.textx + 365, self.texty + 220, self.game.WHITE, self.game.font_name)
            self.game.draw_text('YOU WILL PLAY AS THE', 45, self.textx - 300, self.texty + 290, self.game.WHITE, self.game.font_name)
            self.game.draw_text('WAREHOUSE KEEPER', 45, self.textx + 90, self.texty + 290, self.game.RED, self.game.font_name)
            self.game.draw_text('AND TRY TO COPE', 45, self.textx + 430, self.texty + 290, self.game.WHITE, self.game.font_name)
            self.game.draw_text('WITH THE CHALLENGE, FACING', 45, self.textx - 300, self.texty + 360, self.game.WHITE, self.game.font_name)
            self.game.draw_text('20 MAPS', 45, self.textx + 50, self.texty + 360, self.game.RED, self.game.font_name)
            self.game.draw_text('OF VARYING DIFFICULTY.', 45, self.textx + 350, self.texty + 360, self.game.WHITE, self.game.font_name)
            self.game.draw_text('WE WISH YOU GOOD LUCK!', 45, self.textx, self.texty + 500, self.game.WHITE, self.game.font_name)

            self.blit_screen()


class DiffMenu(Menu):
    """
    Class which represents the diffMenu, inheriting from the Menu class.
    """
    def __init__(self, game):
        """
        :attributes
        titlex, easyx, mediumx, hardx - Buttons initial x coordinates.
        titley, easy, mediumy, hardy - Buttons initial y coordinates.

        :param
        game: class, required
            Game class
        """
        Menu.__init__(self, game)
        self.titlex, self.titley = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200
        self.easyx, self.easyy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.mediumx, self.mediumy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 100
        self.hardx, self.hardy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 200
        self.pointer_rect.midtop = (self.easyx + self.offset, self.easyy)
        self.state = 'Easy'

    def display_menu(self):
        """
        Method that displays the menu. It prints 4 buttons thanks to the draw_text() method.
        It also blits the screen every single frame.
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC_PRESSED:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('SELECT YOUR DIFFICULTY', 85, self.titlex, self.titley, self.game.WHITE, self.game.font_name)
            self.game.draw_text('EASY', 80, self.easyx, self.easyy, self.game.WHITE, self.game.font_name)
            self.game.draw_text('MEDIUM', 80, self.mediumx, self.mediumy, self.game.WHITE, self.game.font_name)
            self.game.draw_text('HARD', 80, self.hardx, self.hardy, self.game.WHITE, self.game.font_name)
            self.draw_pointer()
            self.blit_screen()

    def check_input(self):
        """
        Method that handles changing the currently displayed menu.
        """
        self.move_pointer()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.ESC_PRESSED:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

    def move_pointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.START_KEY:
            if self.state == 'Easy':
                logic.start_the_game(self.game.window, str(randrange(1, 20)) + ".txt", self.game)
            elif self.state == 'Medium':
                logic.start_the_game(self.game.window, str(randrange(21, 40)) + ".txt", self.game)
            else:
                logic.start_the_game(self.game.window, str(randrange(41, 60)) + ".txt", self.game)

        if self.game.DOWN_KEY:
            if self.state == 'Easy':
                self.pointer_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'

            elif self.state == 'Medium':
                self.pointer_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'

            elif self.state == 'Hard':
                self.pointer_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'

        elif self.game.UP_KEY:
            if self.state == 'Easy':
                self.pointer_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'

            if self.state == 'Medium':
                self.pointer_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'

            if self.state == 'Hard':
                self.pointer_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'
