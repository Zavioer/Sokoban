from src.modules.settings import *


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        A box that will move across the screen moved by a warehouse worker.
        
        :param x:
            Position in x-axis.
        :type x: int, required,
        :param y:
            Position in y-axis.
        :type y: int, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = BOX_IMG.convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect()
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

    def collisionWall(self, objectList):
        """
        Check if instance collide with wall in wall group.

        :param objectList:
            Group that contains wall sprites.
        :type objectList: pygame.Sprite.Group, required
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        if self.rect.collidelist(objectList) != -1:
            self.rect.x -= self.moveX
            self.rect.y -= self.moveY

            self.moveX = 0
            self.moveY = 0
            self.blocked = True
        else:
            self.blockedDirection = 'none'

        self.rect.x -= self.moveX
        self.rect.y -= self.moveY

    def collisionBox(self, groupBox):
        """
        Check if instance collide with another box.

        :param groupBox:
            Group that contains Box class sprites.
        :type groupBox: pygame.Sprite.Group, required
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        if self.rect.collidelist(groupBox) != -1:
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

        :param direction:
            Name of direction in which box will be moved. Allowed values
            (north, east, south, west).
        :type direction: str, required
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
    def __init__(self, x, y):
        """
        Class for warehouse walls that block player.

        :param x:
            Position in x-axis.
        :type x: int, required,
        :param y:
            Position in y-axis.
        :type y: int, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = WALL_IMG.convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.char = WALL_CHAR


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Class for warehouse floor on which storekeeper moves.

        :param x:
            Position in x-axis.
        :type x: int, required,
        :param y:
            Position in y-axis.
        :type y: int, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = FLOOR_IMG.convert()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.char = FLOOR_CHAR


class Destination(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Target for the Box class instances

        :param x:
            Position in x-axis.
        :type x: int, required,
        :param y:
            Position in y-axis.
        :type y: int, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = DESTINATION_IMG.convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.char = DESTINATION_CHAR
