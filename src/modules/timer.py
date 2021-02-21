import pygame
import math


class Timer(pygame.sprite.Sprite):
    """
        Class which returns the time (ticks) since the game-start
    """
    def __init__(self, font_name, start):
        pygame.sprite.Sprite.__init__(self)
        self.start = start
        self.passed_time = 0
        self.font_name = font_name
        self.image = font_name.render(f"Time: {self.passed_time}", 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.move(500, 240)

    def update(self):
        self.passed_time = math.ceil((pygame.time.get_ticks() - self.start) / 1000)
        self.image = self.font_name.render(f"Time: {self.passed_time}", 1, (255, 255, 255))
