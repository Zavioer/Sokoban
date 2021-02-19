import pygame
from .functions import load_png


class Destination(pygame.sprite.Sprite):
    """
    Target for box instances
    """
    def __init__(self, x, y):
        """
        :attributes
        state: string
            Tell if box is inside instance or not.

        :param
        x: int
            Initial value in x-axis.
        y: int
            Initial value in y-axis.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('destination.png')
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.width = 50
        self.rect.height = 50
        self.state = 'empty'

    def collide(self, group_box):
        """
        Check if collide with box instance.

        :param
        group_box:
            Group of Box class instances.
        :return
            True if collide or False if not.
        """
        if self.rect.collidelist(group_box) != -1:
            return True
        else:
            return False
