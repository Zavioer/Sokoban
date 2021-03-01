from .menu import *
from .settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fontTitle = 'src/fonts/Future TimeSplitters.otf'
        self.fontName = 'src/fonts/gomarice_no_continue.ttf'
        self.mainMenu = MainMenu(self)
        self.diffMenu = DiffMenu(self)
        self.levelMenu = LevelMenu(self)
        self.legendMenu = LegendMenu(self)
        self.instructionsMenu = InstructionsMenu(self)
        self.creditsMenu = CreditsMenu(self)
        self.currentMenu = self.mainMenu
        self.ESC_PRESSED = False
        self.BLACK, self.WHITE, self.RED = BLACK, WHITE, RED
        self.gameLevel = 1
        self.gamePoints = 0
        
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.ESC_PRESSED:
                self.playing = False
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.currentMenu.runDisplay = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_PRESSED = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_PRESSED, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color, fontName):
        font = pygame.font.Font(fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.display.blit(textSurface, textRect)
