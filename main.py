#!/usr/bin/python
#
# Sokoban
# A simple game with realistic physics and AI
# Released as a part of the Motorola 2020 competition

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import pygame_menu
    from src.modules import player, wall, box, destination, timer
    from pygame.locals import *
except(ImportError):
    print("Couldn't load module. %s" % (ImportError))
    sys.exit(2)

# def set_difficulty(value, difficulty):
#     # Do the job here!
#     pass

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Sokoban Alpha 0')
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Montserrat', 30)

time = timer.Timer()
time.start()

def start_the_game():
# Load game objects
# Fill backgrounds
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    wall_group = pygame.sprite.Group()
    storekeepers = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    dest_group = pygame.sprite.Group()

    with open('./src/boards/1.txt', 'r') as fd:
        boardd = fd.readlines()
        start_x = 0
        start_y = 0

        for rows in boardd:
            start_x = 0
            for column in rows:
                if column == '#':
                    walle = wall.Wall(start_x, start_y)
                    wall_group.add(walle)
                elif column == '$':
                    storekeeper = player.Player(start_x, start_y)
                    storekeepers.add(storekeeper)
                elif column == '+':
                    box_group.add(box.Box(start_x, start_y))
                elif column == '*':
                    dest = destination.Destination(start_x, start_y)
                    dest_group.add(dest)
                start_x += 50
            start_y += 50

    clock = pygame.time.Clock()
    screen.blit(background, (0, 0))
    wall_group.draw(screen)
    pygame.display.flip()

    # Event loop
    while 1:
        if(time.current() % 1000 == 0):
            text = myFont.render('Time: ' + str(time.current() / 1000), True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (screen.get_width() - 50, screen.get_height() - 20)
            screen.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    storekeeper.move(0, -25)
                elif event.key == K_s:
                    storekeeper.move(0, 25)
                elif event.key == K_a:
                    storekeeper.move(-25, 0)
                elif event.key == K_d:
                    storekeeper.move(25, 0)

                storekeeper.collision(wall_group.sprites())
                for boxe in box_group.sprites():
                    boxe.collision_wall(wall_group.sprites(), storekeeper.direction)
                    boxe.collision(storekeeper, storekeeper.direction)

            pygame.display.flip()
            storekeepers.update()

            screen.blit(background, [0, 0])
            wall_group.draw(screen)
            box_group.draw(screen)
            dest_group.draw(screen)
            storekeepers.draw(screen)
            pygame.display.flip()
            clock.tick(60)

def main():
    # Initialize screen
    menu = pygame_menu.Menu(500, 500, 'Sokoban', theme = pygame_menu.themes.THEME_BLUE)
    name = menu.add_text_input('NAME: ', default='')
    menu.add_button('PLAY', start_the_game)
    menu.add_button('QUIT', pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == '__main__':
    main()
