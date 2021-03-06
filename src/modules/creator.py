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
        self.currBlock = 'X'
        self.currColor = BLUE

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

    def get_tile(self):
        return self.currBlock


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        self.color = GREEN
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs) -> None:
        self.image.fill(self.color)

    def change_color(self, name):
        self.color = name


class Button(pygame.sprite.Sprite):
    """
    Utility class for Toolbox.
    """
    def __init__(self, x, y, width, height, bgColor, name, char, color, font,
                 fontColor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(bgColor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.attribute = char
        self.color = color
        text = font.render(name, 1, fontColor)
        text_pos = text.get_rect(center=(width / 2, height / 2))
        self.image.blit(text, text_pos)


class Toolbox(pygame.sprite.Sprite):
    """
    Displays little menu which helps creating new game map.
    """
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.buttons = []
        self.buttonsSprites = pygame.sprite.Group()
        self.width = width
        self.height = height

    def add_button(self, name, char, color):
        self.buttons.append({'name': name, 'char': char, 'color': color})

    def place_buttons(self):
        font = pygame.font.Font('src/fonts/gomarice_no_continue.ttf', 16)
        padding = 25

        for button in self.buttons:
            self.buttonsSprites.add(Button(0, padding,
                                           self.width - 20, 25, BLACK, button['name'],
                                           button['char'], button['color'],
                                           font, WHITE))
            padding += 30

        self.buttonsSprites.draw(self.image)