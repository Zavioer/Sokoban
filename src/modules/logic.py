import pygame
import os
from src.modules import player, wall, box, destination, timer, menu
from pygame.locals import *

def set_difficulty(value, difficulty):
    #Do the job here!
      pass
      
def start_the_game(screen, lvl_name):
    pygame.init()
    my_font = pygame.font.SysFont('Montserrat', 30)

    # Initial sprites groups and map floor
    walls = pygame.sprite.Group()
    storekeepers = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    destinations = pygame.sprite.Group()
    background = pygame.Surface(screen.get_size())
    floor_img = pygame.image.load(os.path.join('src/img/', 'Wall_Black.png'))
    clock = pygame.time.Clock()

    # Load and place objects on map
    with open(os.path.join('./src/boards/', lvl_name), 'r') as fd:
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

    destinations_amount = len(destinations.sprites())
    gamer_timer = pygame.sprite.Group(timer.Timer(my_font, pygame.time.get_ticks()))

    # Event loop
    while 1:
        clock.tick(60)
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

        # Check if all boxes collide with destinations
        placed_boxes = pygame.sprite.groupcollide(box_sprites, destinations, False, False)

        if len(placed_boxes) == destinations_amount:
            print("You won the level!")
            menu.draw_menu(screen)

        # Updating and drawing sprites groups
        storekeepers.update()
        box_sprites.update()
        gamer_timer.update()
        screen.blit(background, (0, 0))

        gamer_timer.draw(screen)
        walls.draw(screen)
        destinations.draw(screen)
        box_sprites.draw(screen)
        storekeepers.draw(screen)

        pygame.display.update()
        pygame.display.flip()
