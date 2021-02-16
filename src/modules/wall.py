import pygame
from .functions import load_png

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('wall.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 50
        self.rect.height = 50
