import os
import pygame
from .settings import *


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []

    def empty_map(self):
        for y in range(0, self.height):
            self.map.append([' '] * self.width)

    def draw_map(self):
        for y in range(0, self.height):
            print(self.map[y])
            print('\n')

    def place_tile(self, x, y, tile):
        self.map[y][x] = tile

    def save_board(self):
        with open(os.path.join('./src/boards/own/', 'text.txt'), 'w') as fd:
            for y in range(0, self.height):
                fd.write(''.join(self.map[y]))
                fd.write('\n')


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.curr_block = 'X'

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

    def get_tile(self):
        return self.curr_block


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((19, 19))
        self.color = GREEN
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs) -> None:
        self.image.fill(self.color)

    def change_color(self, name):
        self.color = name


class Toolbox:
    pass