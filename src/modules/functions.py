import os
import sys
import pygame
def load_png(name):
    """
    Loads image and returns image object
    """
    fullname = os.path.join('src/img/', name)

    image = pygame.image.load(fullname)
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image, image.get_rect()
