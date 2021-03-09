import pygame
import os


# Game settings
FPS = 60
WIDTH = 1280
HEIGHT = 720
midWidth = WIDTH / 2
midHeight = HEIGHT / 2

# Tiles settings
TILE_HEIGHT = 36
TILE_WIDTH = 36
STOREKEEPER_MOVE = 36
WALL_CHAR = 'X'
FLOOR_CHAR = 'a'
STOREKEEPER_CHAR = '@'
BOX_CHAR = '*'
DESTINATION_CHAR = '.'
EMPTY_CHAR = ' '

# Images
STOREKEEPER_IMG = pygame.image.load(os.path.join('./src/img/storekeeper/',
                                                 'storekeeper.png'))
STOREKEEPER_NORTH_IMG = pygame.image.load(os.path.join('./src/img/storekeeper/',
                                                       'storekeeper_north.png'))
STOREKEEPER_EAST_IMG = pygame.image.load(os.path.join('./src/img/storekeeper/',
                                                      'storekeeper_east.png'))
STOREKEEPER_WEST_IMG = pygame.image.load(os.path.join('./src/img/storekeeper/',
                                                      'storekeeper_west.png'))
WALL_IMG = pygame.image.load(os.path.join('./src/img/wall/', 'wall_0.png'))
BOX_IMG = pygame.image.load(os.path.join('./src/img/crate/', 'crate_beige.png'))
FLOOR_IMG = pygame.image.load(os.path.join('./src/img/floor/', 'floor_0.png'))
DESTINATION_IMG = pygame.image.load(os.path.join('./src/img/destination/',
                                                 'destination_0.png'))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# In game HUD
HUD_SIZE = 200

# Create map
BLOCK_SIZE = 25
BOARD_WIDTH = BLOCK_SIZE * 30
BOARD_HEIGHT = BLOCK_SIZE * 20
TOOLBOX_WIDTH = 200

# Fonts
# GOMARINCE_16 = pygame.font.Font('src/fonts/gomarice_no_continue.ttf', 16)

# Utilities
EMPTY_IMG = pygame.Surface((1, 1)).fill(GREEN)
