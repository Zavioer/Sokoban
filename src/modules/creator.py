import os
import time
import pygame
from .settings import *


class Board:
    def __init__(self, width, height):
        """
        Utility class for hidden crating and saving user map to file.
        :param width:
            Map given width. Max number 30.
        :param height:
            Map given width. Max number 20.
        """
        self.width = width
        self.height = height
        self.map = []
        self.availablePlayer = True

    def empty_map(self):
        """
        Fill map attribute with char that represent floor in map.
        """
        for y in range(0, self.height):
            self.map.append([FLOOR_CHAR] * self.width)

    def place_tile(self, x, y, tileChar):
        """
        Place char that represent one of map objects in map attribute.
        :param x:
            Position in x-axis.
        :param y:
            Position in y-axis.
        :param tileChar:
            Character that represents one of map objects.
        """
        self.map[y][x] = tileChar

    def save_board(self, userName):
        """
        Method for saving to created map to .txt file.
        :param userName:
            Map creator nick name.
        """
        currentDate = time.localtime(time.time())
        formatedDate = time.strftime('%H_%M_%S_%d_%m_%Y', currentDate)
        fileName = ''.join((userName, '_', formatedDate, '.txt'))

        with open(os.path.join('./src/boards/own/', fileName), 'w') as fd:
            fd.write(str(self.width) + '\n')
            fd.write(str(self.height) + '\n')
            for y in range(0, self.height):
                fd.write(''.join(self.map[y]))
                fd.write('\n')


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        """
        Utility class for setting graphical and raw map.
        """
        pygame.sprite.Sprite.__init__(self)
        self.currBlock = 'X'
        self.currentImage = WALL_IMG

    def get_tile(self):
        """
        Getter for attribute currBlock.
        :return:
            currBlock
        """
        return self.currBlock


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Graphical representation of block for creation new map.
        :param x:
            Position in x-axis.
        :param y:
            Position in y-axis
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(FLOOR_IMG, (BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.character = 'a'

    def set_image(self, name):
        """
        Setter for attribute self.image. Includes image transformation to
        BLOCK_SIZE const.
        :param name:
            Name on new image to set.
        """
        self.image = name.convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE - 1, BLOCK_SIZE - 1))


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bgColor, name, char, tileImage, font,
                 fontColor):
        """
        Utility class for Toolbox. Created ready do blit button.

        :param x:
            Position in x-axis.
        :param y:
            Position in y-asix.
        :param width:
            Button width.
        :param height:
            Button height.
        :param bgColor:
            Background color on which will be dispay button name.
        :param name:
            Name of button.
        :param char:
            Attribute that represents char for map raw representation.
        :param tileImage:
            Attribute that represent block for map graphical representation.
        :param font:
            Font in which will be render name param.
        :param fontColor:
            Color for font.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(bgColor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.attribute = char
        self.tileImage = tileImage
        text = font.render(name, 1, fontColor)
        text_pos = text.get_rect(center=(width / 2, height / 2))
        self.image.blit(text, text_pos)


class Toolbox(pygame.sprite.Sprite):
    def __init__(self, width, height):
        """
        Container for buttons.

        :param width:
            Width of the container.
        :param height:
            Height of the container.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.buttons = []
        self.buttonsSprites = pygame.sprite.Group()
        self.width = width
        self.height = height

    def add_button(self, name, char, image):
        """
        Method allow add new Button class object to the container.

        :param name:
            Name which will be displayed on button.
        :param char:
            Char that will be set for raw map representation.
        :param image:
            Block that will be set for graphical map representation.
        """
        self.buttons.append({'name': name, 'char': char, 'image': image})

    def place_buttons(self):
        """
        Method that place button on the container, and draw them on in.
        """
        font = pygame.font.Font('src/fonts/gomarice_no_continue.ttf', 16)
        padding = 25

        for button in self.buttons:
            self.buttonsSprites.add(Button(0, padding, self.width - 20, 25,
                                           BLACK, button['name'], button['char'],
                                           button['image'], font, WHITE))
            padding += 30

        self.buttonsSprites.draw(self.image)
