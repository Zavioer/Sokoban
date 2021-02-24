import pygame
from .functions import load_png
from .settings import *


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('floor/floor_1.png')
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT
