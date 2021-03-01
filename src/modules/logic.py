import pygame
import os
import shelve
from pygame.locals import *
from .blocks import Floor, Box, Destination, Wall
from .player import Player
from .hud import HUD
from .hud import Timer
from .creator import Tile
from .creator import Mouse
from .creator import Board
from .game import *
from .settings import *
from src.modules import menu


def start_the_game(screen, lvl_name, game):
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
                floors.add(Floor(start_x, start_y))

                if column == WALL_CHAR:
                    walls.add(Wall(start_x, start_y))
                elif column == STOREKEEPER_CHAR:
                    storekeeper = Player(start_x, start_y)
                    storekeepers.add(storekeeper)
                elif column == BOX_CHAR:
                    boxes.add(Box(start_x, start_y))
                elif column == DESTINATION_CHAR:
                    destinations.add(Destination(start_x, start_y))

                start_x += TILE_WIDTH
            start_y += TILE_HEIGHT

    destinations_amount = len(destinations.sprites())
    gamer_timer = Timer(pygame.time.get_ticks(), my_font)
    hud = HUD(gamer_timer)
    all_sprites = pygame.sprite.Group(walls, destinations, boxes, storekeepers)

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
                elif event.key == K_g:
                    save_board(22, 11, all_sprites, gamer_timer.passed_time)

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

        # Check if all boxes collide with destinations
        placed_boxes = pygame.sprite.groupcollide(boxes, destinations, False, False)

        if len(placed_boxes) == destinations_amount:
            # Correct needed stuck in lvl game
            game.curr_menu = game.main_menu
            game.curr_menu.display_menu()
            game.gameLevel += 1
            break

        # Updating and drawing sprites groups
        storekeepers.update()
        boxes.update()

        screen.fill(BLACK)

        floors.draw(screen)
        all_sprites.draw(screen)
        hud.display_timer(pygame.time.get_ticks())
        hud.display_lvl(lvl_name)
        screen.blit(hud.image, hud.rect)

        pygame.display.update()
        pygame.display.flip()


def save_board(width, height, sprites, time, player_name, lvl_name):
    """
    Function for saving current playing lvl and additional information in to
    shelve file.

    :param width: int
        Current map width.
    :param height: int
        Current map height.
    :param sprites: pygame.sprite.Group
        Group of all sprites in level.
    :param time:
        Time passed from beginning.
    :param player_name: str
        Current playing player name.
    :param lvl_name: str


    :return:
        None
    """
    empty_board = []

    for h in range(height):
        empty_board.append([' '] * width)

    for sprite in sprites:
        empty_board[int(sprite.rect.y / TILE_HEIGHT)][int(sprite.rect.x / TILE_WIDTH)] = sprite.char

    shel_file = shelve.open(os.path.join('./src/saves', 'test'))
    shel_file['mainBoardVar'] = empty_board
    shel_file['timeVar'] = time
    shel_file.close()


def create_map(screen, player_name):
    canvas = pygame.Surface((400, 400))
    canvas.fill(RED)
    clock = pygame.time.Clock()

    mouse = Mouse()
    mouseGrup = pygame.sprite.GroupSingle(mouse)
    allTiles = pygame.sprite.Group()
    playerBoard = Board(20, 20)

    for x in range(0, 400, 20):
        pygame.draw.line(canvas, WHITE, (x, 0), (x, 400))

    for y in range(0, 400, 20):
        pygame.draw.line(canvas, WHITE, (0, y), (400, y))

    for x in range(0, 400, 20):
        for y in range(0, 400, 20):
            allTiles.add(Tile(x, y))

    playerBoard.empty_map()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                for sprite in pygame.sprite.spritecollide(mouseGrup.sprite, allTiles, False):
                    print(f'Collision with rect position ({sprite.rect.x}, {sprite.rect.y})')
                    sprite.change_color(BLUE)
                    playerBoard.place_tile(int(sprite.rect.x / 20), int(sprite.rect.y / 20),
                                            mouse.get_tile())
                playerBoard.draw_map()
            elif event.type == KEYDOWN and event.key == K_s:
                playerBoard.save_board()

        mouseGrup.update()


        screen.blit(canvas, (0, 0))
        allTiles.update()
        allTiles.draw(canvas)
        mouseGrup.draw(canvas)

        pygame.display.update()
        pygame.display.flip()
