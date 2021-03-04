import pygame
from .functions import load_png
from .settings import *


class Box(pygame.sprite.Sprite):
    """
    A box that will move across the screen moved by a warehouse worker.
    """
    def __init__(self, x, y):
        """
        :attributes
        image: pygame.image

        rect: pygame.Rect
            Instance of pygame.Rect object.

        moveX: int
            Placeholder for x-axis offset to move object in update() method.

        moveY: int
            Placeholder for y-axis offset to move object in update() method.

        blocked: bool
            Tells if Box instance is blocked by Wall instance.

        blocked_direction: string
            Direction in which Box instance can't be move.

        blocked_by_box: bool
            Tells if Box instance is blocked by another Box instance.

        :param
        x: int
            Instance start value of x-axis.

        y: int
            Instance start value of y-axis.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = BOX_IMG.convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT
        self.rect.x = x
        self.rect.y = y
        self.moveX = 0
        self.moveY = 0
        self.blocked = False
        self.blockedDirection = 'none'
        self.blockedByBox = False
        self.char = BOX_CHAR

    def update(self):
        """
        Change box position in every frame.
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        self.moveX = 0
        self.moveY = 0

    def collision_wall(self, object_list):
        """
        Check if instance collide with wall in wall group.

        :param
        object_list: pygame.Sprite.Group
            Group that contains wall sprites.

        :return:
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        if self.rect.collidelist(object_list) != -1:
            self.rect.x -= self.moveX
            self.rect.y -= self.moveY

            self.moveX = 0
            self.moveY = 0
            self.blocked = True
        else:
            self.blockedDirection = 'none'

        self.rect.x -= self.moveX
        self.rect.y -= self.moveY

    def collision_box(self, group_box):
        """
        Check if instance collide with another box.

        :param
        group_box: pygame.Sprite.Group
            Group that contains box sprites.

        :return:
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        if self.rect.collidelist(group_box) != -1:
            self.rect.x -= self.moveX
            self.rect.y -= self.moveY
            self.moveX = 0
            self.moveY = 0
            self.blockedByBox = True

        self.rect.x -= self.moveX
        self.rect.y -= self.moveY

    def move(self, direction):
        """
        Prepare instance for changing position. Sets instance possible blocked
        direction.

        :param
        direction: string
            Name of direction in which box will be moved. Allowed values
            (north, east, south, west).
        :return:
        """
        if direction == 'north':
            self.moveY -= STOREKEEPER_MOVE
        elif direction == 'south':
            self.moveY += STOREKEEPER_MOVE
        elif direction == 'east':
            self.moveX += STOREKEEPER_MOVE
        elif direction == 'west':
            self.moveX -= STOREKEEPER_MOVE

        self.blockedDirection = direction


class Wall(pygame.sprite.Sprite):
    """
    Class for warehouse walls that block player.
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
        self.image = WALL_IMG.convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))

        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT
        self.rect.x = x
        self.rect.y = y
        self.char = WALL_CHAR


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = FLOOR_IMG.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT
        self.char = FLOOR_CHAR


class Destination(pygame.sprite.Sprite):
    """
    Target for box instances
    """
    def __init__(self, x, y):
        """
        :attributes
        state: string
            Tells if the box is inside instance or not.

        :param
        x: int
            Initial value in x-axis.
        y: int
            Initial value in y-axis.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = DESTINATION_IMG.convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT
        self.rect.x = x
        self.rect.y = y
        self.char = DESTINATION_CHAR
