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
    from src.modules.functions import load_png
except ImportError:
    print(f"Could not load module: {ImportError}")
    sys.exit(2)

def set_difficulty(value, difficulty):
    #Do the job here!
      pass

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Sokoban Alpha 0')
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Montserrat', 30)

time = timer.Timer()
time.start()

def start_the_game():
    # Initial sprites groups and map floor
    walls = pygame.sprite.Group()
    storekeepers = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    destinations = pygame.sprite.Group()
    background = pygame.Surface(screen.get_size())
    floor_img = pygame.image.load(os.path.join('src/img/', 'Wall_Black.png'))

    # Load and place objects on map
    with open('./src/boards/5.txt', 'r') as fd:
        board = fd.readlines()
        start_y = 0

        for rows in board:
            start_x = 0
            for column in rows:
                background.blit(floor_img, (start_x, start_y))

                if column == 'X':
                    walls.add(wall.Wall(start_x, start_y))
                elif column == '@':
                    storekeeper = player.Player(start_x, start_y)
                    storekeepers.add(storekeeper)
                elif column == '*':
                    box_sprites.add(box.Box(start_x, start_y))
                elif column == '.':
                    destinations.add(destination.Destination(start_x, start_y))

                start_x += 50
            start_y += 50

    clock = pygame.time.Clock()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    storekeeper.move(0, -50)
                elif event.key == K_s:
                    storekeeper.move(0, 50)
                elif event.key == K_a:
                    storekeeper.move(-50, 0)
                elif event.key == K_d:
                    storekeeper.move(50, 0)

                storekeeper.collision(walls.sprites())

                for box_sprite in box_sprites.sprites():
                    box_sprites_copy = box_sprites.copy()
                    box_sprites_copy.remove(box_sprite)
                    storekeeper.collision_box(box_sprite)

                    if storekeeper.box_collision:
                        box_sprite.move(storekeeper.direction)

                        box_sprite.collision_wall(walls.sprites())
                        box_sprite.collision_box(box_sprites_copy.sprites())

                        if box_sprite.blocked_by_box:
                            storekeeper.move(-storekeeper.movex, -storekeeper.movey)
                        if box_sprite.blocked and storekeeper.direction == box_sprite.blocked_direction:
                            storekeeper.move(-storekeeper.movex, -storekeeper.movey)

                        storekeeper.box_collision = False

            for destination_sprite in destinations.sprites():
                if destination_sprite.collide(box_sprites.sprites()):
                    destination_sprite.state = 'full'
                else:
                    destination_sprite.state = 'empty'

            if time.current() % 1000 == 0:
                text = myFont.render('Time: ' + str(time.current() / 1000), True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (screen.get_width() - 50, screen.get_height() - 20)
                screen.blit(text, textRect)

            # Updating and drawing sprites groups
            storekeepers.update()
            box_sprites.update()

            screen.blit(background, (0, 0))
            walls.draw(screen)
            destinations.draw(screen)
            box_sprites.draw(screen)
            storekeepers.draw(screen)

            pygame.display.update()
            pygame.display.flip()

            clock.tick(60)


def main():
    # Initialize screen
    menu = pygame_menu.Menu(720, 1280, 'SOKOBAN 1.0.0', theme = pygame_menu.themes.THEME_SOLARIZED)
    name = menu.add_text_input('NAME: ', default='')
    menu.add_button('PLAY', start_the_game)
    menu.add_button('QUIT', pygame_menu.events.EXIT)
    menu.add_button('CHOOSE LEVEL', set_difficulty)
    menu.mainloop(screen)


if __name__ == '__main__':
    main()
