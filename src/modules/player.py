import os
import pygame
from .functions import load_png
from .settings import *


class Player(pygame.sprite.Sprite):
    """
    Class which represents a player. Loads image and sets up instance
    in coordinate system.
    """
    def __init__(self, x, y):
        """
        :attributes
        image: pygame.Image
            Image that represents player instance.
        rect: pygame.Rect
            Pygame Rect class of player instance.
        direction: string
            Direction in which player moves. Allowed values(north, east, south,
            west)
        boxCollision: bool
            State of checking if player collides with Box instance.

        :param
        x: int, required
            Player initial x coordinate.
        y: int, required
            Player initial y coordinate.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = STOREKEEPER_IMG.convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moveX = 0
        self.moveY = 0
        self.direction = 'none'
        self.boxCollision = False
        self.char = STOREKEEPER_CHAR

    def update(self):
        """
        Method that update player position in every frame.
        """
        self.boxCollision = False

        self.rect.x += self.moveX
        self.rect.y += self.moveY

        self.moveX = 0
        self.moveY = 0

    def move(self, x, y):
        """
        Changes object position in coordinate system to given offset.

        :param
        x: int, required
            Offset to move in x-axis.
        y: int, required
            Offset to move in y-axis.
        """
        if x > 0:
            self.direction = 'east'
        elif x < 0:
            self.direction = 'west'

        if y > 0:
            self.direction = 'south'
        elif y < 0:
            self.direction = 'north'

        self.changePosition(self.direction)

        self.moveX += x
        self.moveY += y

    def collision(self, object_list):
        """
        Check if next player position will collide with object in list.

        :param
        object_list: list, required
            List of objects which probable collision.
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        if self.rect.collidelist(object_list) != -1:
            self.rect.x -= self.moveX
            self.rect.y -= self.moveY

            self.moveX = 0
            self.moveY = 0

        self.rect.x -= self.moveX
        self.rect.y -= self.moveY

    def collisionBox(self, box):
        """
        Check if instance collide with box.

        :param
        box: pygame.Rect
            Rectangle that represent Box instance.
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        if self.rect.colliderect(box):
            self.boxCollision = True

        self.rect.x -= self.moveX
        self.rect.y -= self.moveY

    def changePosition(self, direction):
        """
        Change player's move animation on move.

        :param
        direction: string, required
            Direction in which player moves.
        """
        if direction == 'north':
            self.image = STOREKEEPER_NORTH_IMG
        elif direction == 'east':
            self.image = STOREKEEPER_EAST_IMG
        elif direction == 'west':
            self.image = STOREKEEPER_WEST_IMG
        else:
            self.image = STOREKEEPER_IMG

        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))