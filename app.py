#!/usr/bin/python
#
# Sokoban
# A simple game with realistic physics and AI
# Released as a part of the Motorola 2020 competition


import pygame
from src.modules import menu
from src.modules.settings import *


def main():
    # Initialization
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sokoban Alpha 0')

    pygame.init()
    menu.draw_menu(screen)


if __name__ == '__main__':
    main()
