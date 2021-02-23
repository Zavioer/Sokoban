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

        movex: int
            Placeholder for x-axis offset to move object in update() method.

        movey: int
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
        self.image, self.rect = load_png('box.png')
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect.width = TILE_WIDTH
        self.rect.height = TILE_HEIGHT
        self.rect.x = x
        self.rect.y = y
        self.movex = 0
        self.movey = 0
        self.blocked = False
        self.blocked_direction = 'none'
        self.blocked_by_box = False

    def update(self):
        """
        Change box position in every frame.
        """
        self.rect.x += self.movex
        self.rect.y += self.movey

        self.movex = 0
        self.movey = 0

    def collision_wall(self, object_list):
        """
        Check if instance collide with wall in wall group.

        :param
        object_list: pygame.Sprite.Group
            Group that contains wall sprites.

        :return:
        """
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.rect.collidelist(object_list) != -1:
            self.rect.x -= self.movex
            self.rect.y -= self.movey

            self.movex = 0
            self.movey = 0
            self.blocked = True
        else:
            self.blocked_direction = 'none'

        self.rect.x -= self.movex
        self.rect.y -= self.movey

    def collision_box(self, group_box):
        """
        Check if instance collide with another box.

        :param
        group_box: pygame.Sprite.Group
            Group that contains box sprites.

        :return:
        """
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.rect.collidelist(group_box) != -1:
            self.rect.x -= self.movex
            self.rect.y -= self.movey
            self.movex = 0
            self.movey = 0
            self.blocked_by_box = True

        self.rect.x -= self.movex
        self.rect.y -= self.movey

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
            self.movey -= STOREKEEPER_MOVE
        elif direction == 'south':
            self.movey += STOREKEEPER_MOVE
        elif direction == 'east':
            self.movex += STOREKEEPER_MOVE
        elif direction == 'west':
            self.movex -= STOREKEEPER_MOVE

        self.blocked_direction = direction
