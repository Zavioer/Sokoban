import pygame, sys
from src.modules import logic


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
        self.offset = - 100

    def draw_pointer(self):
        """
        Method that draws the pointer on the display.
        """
        self.game.draw_text('X', 50, self.pointer_rect.x - 50, self.pointer_rect.y, self.game.WHITE)

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
        startx, levelx, instructionsx, creditsx, quitx - Buttons initial x coordinates.
        starty, levely, instructionsy, creditsy, quity - Buttons initial y coordinates.
        :param
        game: class, required
            Game class
        """
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h
        self.levelx, self.levely = self.mid_w, self.mid_h + 100
        self.instructionsx, self.instructionsy = self.mid_w, self.mid_h + 200
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 300
        self.quitx, self.quity = self.mid_w, self.mid_h + 400
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
            self.game.draw_text("SOKOBAN", 150, self.startx, self.starty - 300, self.game.WHITE)
            self.game.draw_text("Start Game", 90, self.startx, self.starty, self.game.WHITE)
            self.game.draw_text("Load Level", 90, self.levelx, self.levely, self.game.WHITE)
            self.game.draw_text("Instructions", 90, self.instructionsx, self.instructionsy, self.game.WHITE)
            self.game.draw_text("Credits", 90, self.creditsx, self.creditsy, self.game.WHITE)
            self.game.draw_text("Quit", 90, self.quitx, self.quity, self.game.WHITE)
            self.draw_pointer()
            self.blit_screen()

    def move_pointer(self):
        """
        Method that includes pointer's movement logic. Moreover, it includes an end event handler.
        """
        if self.game.START_KEY == True:
            if self.state == 'Start':
                logic.start_the_game(self.game.window, "61.txt")
            if self.state == 'Quit':
                sys.exit()
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
                self.game.playing = True
            elif self.state == 'Level':
                self.game.curr_menu = self.game.level
            elif self.state == 'Instructions':
                # self.game.curr_menu = self.game.instructions
                pass
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
        self.level = ''

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
            self.game.draw_text("Choose module: ", 170, self.mid_w, self.mid_h - 300, self.game.WHITE)
            self.game.draw_text("Module 1", 80, self.firstx, self.firsty, self.game.WHITE)
            self.game.draw_text("Module 2", 80, self.secondx, self.secondy, self.game.WHITE)
            self.game.draw_text("Module 3", 80, self.thirdx, self.thirdy, self.game.WHITE)
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
        if self.game.START_KEY == True:
            self.level = self.state
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
        self.titlex, self.titley = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 350
        self.fauthorx, self.fauthory = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10 - 200
        self.sauthorx, self.sauthory = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 80
        self.partx, self.party = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 100
        self.tournamentx, self.tournamenty = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 200
        self.tasksx, self.tasksy = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 300
        self.copyrightx, self.copyrighty = self.game.DISPLAY_W - 300, self.game.DISPLAY_H - 50

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
            self.game.draw_text('THE GAME HAS BEEN WRITTEN BY', 100, self.titlex, self.titley, self.game.WHITE)
            self.game.draw_text('PIOTR BATOR', 80, self.fauthorx, self.fauthory, self.game.WHITE)
            self.game.draw_text('GABRIEL BRZOSKWINIA', 80, self.sauthorx, self.sauthory, self.game.WHITE)
            self.game.draw_text('AS A PART OF', 80, self.partx, self.party, self.game.WHITE)
            self.game.draw_text('THE MOTOROLA SCIENCE CUP', 80, self.tournamentx, self.tournamenty, self.game.RED)
            self.game.draw_text('COMPETITION TASKS', 80, self.tasksx, self.tasksy, self.game.WHITE)
            self.game.draw_text('2021 © ALL RIGHTS RESERVED', 60, self.copyrightx, self.copyrighty, self.game.WHITE)

            self.blit_screen()

