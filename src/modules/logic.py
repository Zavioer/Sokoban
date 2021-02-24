import pygame
import os
from src.modules import player, wall, box, destination, floor, timer, menu, camera
from .game import *
from pygame.locals import *
from .settings import *


# FEATURE TO RELEASE -> HOW TO PASS THE MODULE FROM THE LEVELMENU CLASS?

def start_the_game(screen, lvl_name):
    pygame.init()
    my_font = pygame.font.SysFont('Montserrat', 30)

    # Initial sprites groups and map floor
    walls = pygame.sprite.Group()
    storekeepers = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    destinations = pygame.sprite.Group()

    floors = pygame.sprite.Group()
    clock = pygame.time.Clock()

    # Load and place objects on the map
    with open(os.path.join('./src/boards/', lvl_name), 'r') as fd:
        board = fd.readlines()
        start_y = 0

        for rows in board:
            start_x = 0
            for column in rows:
                floors.add(floor.Floor(start_x, start_y))

                if column == 'X':
                    walls.add(wall.Wall(start_x, start_y))
                elif column == '@':
                    storekeeper = player.Player(start_x, start_y)
                    storekeepers.add(storekeeper)
                elif column == '*':
                    boxes.add(box.Box(start_x, start_y))
                elif column == '.':
                    destinations.add(destination.Destination(start_x, start_y))

                start_x += TILE_WIDTH
            start_y += TILE_HEIGHT

    destinations_amount = len(destinations.sprites())
    gamer_timer = pygame.sprite.Group(timer.Timer(my_font, pygame.time.get_ticks()))
    all_sprites = pygame.sprite.Group(floors, walls, destinations, boxes, storekeepers)
    player_camera = camera.Camera(1080, 720)

    # Event loop
    while 1:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    storekeeper.move(0, -STOREKEEPER_MOVE)
                elif event.key == K_s:
                    storekeeper.move(0, STOREKEEPER_MOVE)
                elif event.key == K_a:
                    storekeeper.move(-STOREKEEPER_MOVE, 0)
                elif event.key == K_d:
                    storekeeper.move(STOREKEEPER_MOVE, 0)

        storekeeper.collision(walls.sprites())

        for box_sprite in boxes.sprites():
            boxes_copy = boxes.copy()
            boxes_copy.remove(box_sprite)
            storekeeper.collision_box(box_sprite)

            if storekeeper.box_collision:
                box_sprite.move(storekeeper.direction)

                box_sprite.collision_wall(walls.sprites())
                box_sprite.collision_box(boxes_copy.sprites())

                if box_sprite.blocked_by_box:
                    storekeeper.move(-storekeeper.movex, -storekeeper.movey)
                if box_sprite.blocked and storekeeper.direction == box_sprite.blocked_direction:
                    storekeeper.move(-storekeeper.movex, -storekeeper.movey)

                storekeeper.box_collision = False

        for destination_sprite in destinations.sprites():
            if destination_sprite.collide(boxes.sprites()):
                destination_sprite.state = 'full'
            else:
                destination_sprite.state = 'empty'

        # Check if all boxes collide with destinations
        placed_boxes = pygame.sprite.groupcollide(boxes, destinations, False, False)

        if len(placed_boxes) == destinations_amount:
            print("You won the level!")
            self.game.curr_menu = self.game.main_menu
            self.game.Game.curr_menu.display_menu()

        # Updating and drawing sprites groups
        storekeepers.update()
        boxes.update()
        gamer_timer.update()
        player_camera.update(storekeeper)

        screen.fill(BLACK)
        for sprite in all_sprites:
            screen.blit(sprite.image, player_camera.apply(sprite))
        gamer_timer.draw(screen)

        pygame.display.update()
        pygame.display.flip()
