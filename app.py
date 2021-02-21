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
from src.modules import logic
from pygame.locals import *
from src.modules.functions import load_png



def set_difficulty(value, difficulty):
    #Do the job here!
      pass


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Sokoban Alpha 0')

pygame.init()

def main():
    # Initialize screen
    menu = pygame_menu.Menu(720, 1280, 'SOKOBAN 1.0.0', theme=pygame_menu.themes.THEME_SOLARIZED)
    name = menu.add_text_input('NAME: ', default='')
    menu.add_button('PLAY', logic.start_the_game(screen, '1.txt'))
    menu.add_button('QUIT', pygame_menu.events.EXIT)
    menu.add_button('CHOOSE LEVEL', set_difficulty)
    menu.mainloop(screen)


if __name__ == '__main__':
    main()
