#!/usr/bin/python
#
# Sokoban
# A simple game with realistic physics and AI
# Released as a part of the Motorola 2020 competition

import sys, random, math, os, getopt, pygame
from src.modules.game import Game
from pygame.locals import *
# from src.modules import logic, menu
# from src.modules.functions import load_png


def main():
    game = Game()
    while game.running:
        game.curr_menu.display_menu()
        game.game_loop()


if __name__ == '__main__':
    main()
