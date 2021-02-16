import pygame
from .functions import load_png

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('box.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.x = x
        self.rect.y = y
        self.moveable = True
        self.rect.height = 50
        self.rect.width = 50

    def update(self):
        pass

    def collision(self, player, direction):
        if self.rect.colliderect(player) and self.moveable:
            self.move(direction)

    def move(self, direction):
        if direction == 'north':
            self.rect.y -= 50
        elif direction == 'south':
            self.rect.y += 50
        elif direction == 'east':
            self.rect.x += 50
        elif direction == 'west':
            self.rect.x -= 50