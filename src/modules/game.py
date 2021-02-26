from .menu import *
from .settings import *


class Game:
    def __init__(self):
        pygame.init()
        self. running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self. DISPLAY_H = WIDTH, HEIGHT
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_title = "src/fonts/Future TimeSplitters.otf"
        self.font_name = "src/fonts/gomarice_no_continue.ttf"
        self.main_menu = MainMenu(self)
        self.level = LevelMenu(self)
        self.legend_menu = LegendMenu(self)
        self.instructions = InstructionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.ESC_PRESSED = False
        self.BLACK, self.WHITE, self.RED = BLACK, WHITE, RED

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
                self.curr_menu.run_display = False

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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_PRESSED = False, False, False, False, False

    def draw_text(self, text, size, x, y, color, fontname):
        font = pygame.font.Font(fontname, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
