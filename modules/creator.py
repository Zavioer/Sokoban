import time
from collections import Counter
from settings import *


class Board:
    def __init__(self, width, height):
        """
        Utility class for hidden crating and saving user map to file.

        :param width:
            Map given width. Max number 30.
        :type width: int, required
        :param height:
            Map given width. Max number 20.
        :type height: int, required
        """
        self.width = width
        self.height = height
        self.map = []
        self.availablePlayer = True

    def emptyMap(self):
        """
        Fill map attribute with char that represent floor in map.
        """
        for y in range(0, self.height):
            self.map.append([FLOOR_CHAR] * self.width)

    def placeTile(self, x, y, tileChar):
        """
        Place char that represent one of map objects in map array.

        :param x:
            Position in x-axis.
        :type x: int, required
        :param y:
            Position in y-axis.
        :type y: int, required
        :param tileChar:
            Character that represents one of map objects.
        :type tileChar: str, required
        """
        self.map[y][x] = tileChar

    def saveBoard(self, mapName, userName):
        """
        Method for saving the new created map to .txt file.

        :param userName:
            Map creator nick name.
        :type userName: str, required
        """
        currentDate = time.localtime(time.time())
        formatedDate = time.strftime('%H_%M_%S_%d_%m_%Y', currentDate)
        fileName = ''.join((mapName, '_', formatedDate, '_', userName, '.txt'))

        with open(os.path.join('./src/boards/own/', fileName), 'w') as fd:
            fd.write(str(self.width) + '\n')
            fd.write(str(self.height) + '\n')

            for y in range(0, self.height):
                fd.write(''.join(self.map[y]))
                fd.write('\n')

    def checkAssets(self):
        """
        Method for checking in all available blocks were placed.

        :return:

        """
        assets = Counter()

        for line in self.map:
            assets.update(line)

        assets = dict(assets)

        if STOREKEEPER_CHAR not in assets.keys():
            assets[STOREKEEPER_CHAR] = 0

        if WALL_CHAR not in assets.keys():
            assets[WALL_CHAR] = 0

        if FLOOR_CHAR not in assets.keys():
            assets[FLOOR_CHAR] = 0

        if BOX_CHAR not in assets.keys():
            assets[BOX_CHAR] = 0

        if DESTINATION_CHAR not in assets.keys():
            assets[DESTINATION_CHAR] = 0

        for key in assets.keys():
            if assets[key] < 1:
                return False

        return True

    def destinationsEqualsBoxes(self):
        """
        Utility method for checking if boxes and destination amount is equal.

        :return:
        """
        assets = Counter()

        for line in self.map:
            assets.update(line)

        assets = dict(assets)

        if BOX_CHAR not in assets.keys():
            assets[BOX_CHAR] = 0

        if DESTINATION_CHAR not in assets.keys():
            assets[DESTINATION_CHAR] = 0

        if assets[BOX_CHAR] < assets[DESTINATION_CHAR]:
            return False

        return True


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        """
        Utility class for setting graphical and raw map.
        """
        pygame.sprite.Sprite.__init__(self)
        self.currBlock = 'X'
        self.currentImage = WALL_IMG

    def getTile(self):
        """
        Getter for attribute currBlock.

        :return:
            Board.currBlock
        """
        return self.currBlock


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Graphical representation of block for creation the new map.

        :param x:
            Position in x-axis.
        :type x: int, required
        :param y:
            Position in y-axis
        :type y: int, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(FLOOR_IMG, (BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.character = 'a'

    def setImage(self, name):
        """
        Setter for attribute self.image. Includes image transformation to
        BLOCK_SIZE const.

        :param name:
            Name on new image to set.
        :type name: str, required
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
        :type x: int, required,
        :param y:
            Position in y-axis.
        :type y: int, required
        :param width:
            Button width.
        :type width: int, required
        :param height:
            Button height.
        :type width: int, required
        :param bgColor:
            Background color on which will be display button name.
        :type bgColor: tuple, required
        :param name:
            Name of button.
        :type name: str, required
        :param char:
            Attribute that represents char for map raw representation.
        :type char: str, required
        :param tileImage:
            Attribute that represent block for map graphical representation.
        :type tileImage: pygame.Surface, required
        :param font:
            Font in which will be render name param.
        :type font: pygame.Font, required
        :param fontColor:
            Color for font.
        :type fontColor: tuple, required
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
        :type width: int, required
        :param height:
            Height of the container.
        :type height: int, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.buttons = []
        self.buttonsSprites = pygame.sprite.Group()
        self.width = width
        self.height = height

    def addButton(self, name, char, image):
        """
        Method allows add a new Button object to the container.

        :param name:
            Name which will be displayed on button.
        :type name: str, required
        :param char:
            Char that will be set for raw map representation.
        :type char: str, required
        :param image:
            Block that will be set for graphical map representation.
        :type image: pygame.Surface, required
        """
        self.buttons.append({'name': name, 'char': char, 'image': image})

    def placeButtons(self):
        """
        Method that place button on the container, and draw them on in.
        """
        font = pygame.font.Font('src/fonts/gomarice_no_continue.ttf', 16)
        padding = 25

        for button in self.buttons:
            self.buttonsSprites.add(Button(20, padding, self.width - 40, 25,
                                           BLACK, button['name'], button['char'],
                                           button['image'], font, WHITE))
            padding += 30

        self.buttonsSprites.add(Button(20, padding + 470, self.width - 40, 25, BLACK, 'save map', button['char'], button['image'], font, WHITE))
        self.buttonsSprites.add(Button(20, padding + 500, self.width - 40, 25, BLACK, 'quit', button['char'], button['image'], font, WHITE))
        self.buttonsSprites.draw(self.image)
