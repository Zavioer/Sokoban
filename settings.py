import pygame
import os
from pathlib import Path


# Paths
BASE_DIR = os.path.split(os.path.abspath(__file__))[0]
IMAGES_DIR = Path(BASE_DIR, 'src/img')
SAVES_DIR = Path(BASE_DIR, 'src/saves')
FONTS_DIR = Path(BASE_DIR, 'src/fonts')

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
STOREKEEPER_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'storekeeper.png'))
STOREKEEPER_NORTH_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'storekeeper_north.png'))
STOREKEEPER_EAST_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'storekeeper_east.png'))
STOREKEEPER_WEST_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'storekeeper_west.png'))
WALL_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'wall_0.png'))
BOX_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'crate_beige.png'))
FLOOR_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'floor_0.png'))
DESTINATION_IMG = pygame.image.load(os.path.join(IMAGES_DIR, 'destination_0.png'))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = pygame.Color('gray15')
LIGHTSKYBLUE = pygame.Color('lightskyblue3')

# In game HUD size
HUD_WIDTH = 280
HUD_HEIGHT = 150

# Create map
BLOCK_SIZE = 25
BOARD_WIDTH = BLOCK_SIZE * 30
BOARD_HEIGHT = BLOCK_SIZE * 20
TOOLBOX_WIDTH = 200

# Fonts
GOMARINCE = os.path.join(FONTS_DIR, 'gomarice_no_continue.ttf')
TIME_SPLITTERS = os.path.join(FONTS_DIR, 'Future TimeSplitters.otf')
# Utilities
SCORE_BASE = 100

# EMPTY_IMG = pygame.Surface((1, 1)).fill(GREEN)

# Flags
MODULE_I = 'MODULEI'
MODULE_II = 'MODULEII'
MODULE_III = 'MODULEIII'
RESTORE = 'RESTORE'
