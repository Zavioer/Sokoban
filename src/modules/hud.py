import pygame
import math
from .settings import *


class HUD(pygame.sprite.Sprite):
    """
    Class for HUD which displays information about current game.
    """
    def __init__(self, timer):
        """
        :param timer: Timer
            Timer object for time handling.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((HUD_SIZE, WIDTH))
        self.image.fill(RED)
        self.timer = timer
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - HUD_SIZE
        self.padding = 25

    def display_lvl(self, lvl_number):
        clean_name = lvl_number[:lvl_number.find('.')]
        font = pygame.font.Font(None, 32)
        text = font.render(f"Level number: {clean_name}", 1, WHITE)
        lvl_pos = text.get_rect(y=self.padding, centerx=self.image.get_width() / 2)
        self.image.blit(text, lvl_pos)

    def display_timer(self, passed_ticks):
        self.image.fill(RED)
        self.timer.set_position(self.image.get_width() / 2, self.padding * 2)
        self.timer.update(passed_ticks)

        self.image.blit(self.timer.image, self.timer.rect)


class Timer(pygame.sprite.Sprite):
    """
        Class which returns the time (ticks) since the game-start
    """
    def __init__(self, start, font_name):
        pygame.sprite.Sprite.__init__(self)
        self.start = start
        self.passed_time = 0
        self.font_name = font_name
        self.x = 0
        self.y = 0

    def update(self, ticks):
        self.passed_time = math.ceil((ticks - self.start) / 1000)
        self.image = self.font_name.render(f"Time: {self.passed_time}", 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.y = self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y
