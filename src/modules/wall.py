import pygame
from .functions import load_png
from .settings import *


class Wall(pygame.sprite.Sprite):
    """
    Class for warehouse walls which blocks player.
    """
    def __init__(self, x, y):
        """
        :param
        x: int
            Initial value in x-axis.
        y: int
            Initial value in y-axis.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('CrateDark_Black.png')
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT
        self.rect.x = x
        self.rect.y = y

