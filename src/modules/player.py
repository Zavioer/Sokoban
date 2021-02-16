import pygame
import os
from .functions import load_png

class Player(pygame.sprite.Sprite):
    """
    Class witch represent player. Loads image, and set up instance 
    in coordinate system.

    Parameters
    ----------
    x: int, required
        Player initial x coordinate.
    y: int, required
        Player initial y coordinate.

    Returns
    -------

    Example
    -------
    """
    def __init__(self, x, y):
        self.movex = 0
        self.movey = 0
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('player.png')
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.state = 'move'
        self.rect.width = 50
        self.rect.height = 50
        self.direction = 'none'

    def update(self):
        self.rect.x += self.movex
        self.movex = 0

        self.rect.y += self.movey
        self.movey = 0

    """
    Change object position in coordinate system to given offset.

    Parameters
    ----------
    x: int, required
        Offset to move in x asix.
    y: int, required
        Offset to move in y asix.
    """
    def move(self, x, y):
        if x > 0:
            self.direction = 'east'
        elif x < 0:
            self.direction = 'west'
        
        if y > 0:
            self.direction = 'south'
        elif y < 0:
            self.direction = 'north'

        self.change_position(self.direction)

        self.movex += x
        self.movey += y

    """
    Check if next player position will colidate with object in list.

    Parameters
    ----------
    object_list: list, required
        List of objects wich probable collision.
    """
    def collision(self, object_list):
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.rect.collidelist(object_list) != -1:
            self.rect.x -= self.movex
            self.rect.y -= self.movey
            
            self.movex = 0
            self.movey = 0

    def change_position(self, direction):
        if direction == 'north':
            self.image = pygame.image.load(os.path.join('src/img/', 'player_north.png'))
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif direction == 'east':
            self.image = pygame.image.load(os.path.join('src/img/', 'player_east.png'))
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif direction == 'south':
            self.image = pygame.image.load(os.path.join('src/img/', 'player.png'))
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif direction == 'west':
            self.image = pygame.image.load(os.path.join('src/img/', 'player_west.png'))
            self.image = pygame.transform.scale(self.image, (50, 50))
        else:
            self.image = pygame.image.load(os.path.join('src/img/', 'player.png'))
            self.image = pygame.transform.scale(self.image, (50, 50))