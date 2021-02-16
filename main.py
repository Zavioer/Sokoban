#!/usr/bin/python
import sys
import random
import math
import os
import getopt
import pygame
from src.modules import player, wall, box, destination
from pygame.locals import *

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Sokoban Alpha 0')

    # Load game objects
    

    # Fill backgrounds
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    wall_group = pygame.sprite.Group()
    magz = pygame.sprite.Group()
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
                    magazynier = player.Player(start_x, start_y)
                    magz.add(magazynier)
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
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    magazynier.move(0, -25)
                elif event.key == K_s:
                    magazynier.move(0, 25)
                elif event.key == K_a:
                    magazynier.move(-25, 0)
                elif event.key == K_d:
                    magazynier.move(25, 0)

                magazynier.collision(wall_group.sprites())
                for boxe in box_group.sprites():
                    boxe.collision(magazynier, magazynier.direction)
    
            pygame.display.flip()
            magz.update()
            
            screen.blit(background, [0, 0])
            wall_group.draw(screen)
            box_group.draw(screen)
            dest_group.draw(screen)
            magz.draw(screen)
            pygame.display.flip()
            clock.tick(60)
            


if __name__ == '__main__': 
    main()