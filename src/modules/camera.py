import pygame
from .settings import *


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, target):
        return target.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - (WIDTH - 200)), x)
        y = max(-(self.height - (HEIGHT - 250)), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
