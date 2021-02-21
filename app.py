#!/usr/bin/python
#
# Sokoban
# A simple game with realistic physics and AI
# Released as a part of the Motorola 2020 competition

import sys
import random
import math
import os
import getopt
import pygame
import pygame_menu
from src.modules import logic, menu
from pygame.locals import *
from src.modules.functions import load_png

def main():
    # Initialization
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Sokoban Alpha 0')

    pygame.init()
    menu.draw_menu(screen)
    
if __name__ == '__main__':
    main()
