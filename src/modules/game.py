from .menu import *
from .settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.ESC_PRESSED = False
        self.RIGHT_KEY = False
        self.LEFT_KEY = False
        self.S_KEY = False
        self.W_KEY = False
        self.logicState = True

        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        self.fontTitle = 'src/fonts/Future TimeSplitters.otf'
        self.fontName = 'src/fonts/gomarice_no_continue.ttf'
        self.mainMenu = MainMenu(self)
        self.inputMenu = InputName(self)
        self.diffMenu = DiffMenu(self)
        self.rankMenu = RankMenu(self)
        self.levelMenu = LevelMenu(self)
        self.legendMenu = LegendMenu(self)
        self.instructionsMenu = InstructionsMenu(self)
        self.creditsMenu = CreditsMenu(self)
        self.saveGameMenu = SaveGameMenu(self)
        self.currentMenu = self.mainMenu
        self.BLACK, self.WHITE, self.RED = BLACK, WHITE, RED
        self.gameLevel = 1
        self.gamePoints = 0
        self.playerName = ''
        self.currentLevel = 0
        self.currentPlayerState = {'width': 0, 'height': 0, 'map': [], 'time': 0}
        self.previousState = 'Start'

    def check_events(self):
        if self.running:
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
                    if event.key == pygame.K_s:
                        self.S_KEY = True
                    if event.key == pygame.K_w:
                        self.W_KEY = True

    def reset_keys(self):
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.ESC_PRESSED = False
        self.RIGHT_KEY = False
        self.LEFT_KEY = False
        self.S_KEY = False
        self.W_KEY = False

    def draw_text(self, text, size, x, y, color, fontName):
        font = pygame.font.Font(fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.display.blit(textSurface, textRect)
