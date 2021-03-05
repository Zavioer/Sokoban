import pygame
import os
import time
import shelve
from pygame.locals import *
from .blocks import Floor, Box, Destination, Wall
from .player import Player
from .hud import HUD, Timer
from .game import *
from .settings import *
from src.modules import menu


def start_the_game(screen, lvlName, game, points):
    start = time.time()
    myFont = pygame.font.SysFont('Montserrat', 30)


    # Initial sprites groups and map floor
    walls = pygame.sprite.Group()
    storekeepers = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    destinations = pygame.sprite.Group()

    floors = pygame.sprite.Group()
    clock = pygame.time.Clock()

    # Load and place objects on the map
    with open(os.path.join('./src/boards/', lvlName), 'r') as fd:
        w = int(fd.readline())
        h = int(fd.readline())
        startY = 0

        for rows in fd:
            startX = 0
            for column in rows:
                # floors.add(Floor(startX, startY))

                if column == WALL_CHAR:
                    walls.add(Wall(startX, startY))
                elif column == STOREKEEPER_CHAR:
                    storekeeper = Player(startX, startY)
                    storekeepers.add(storekeeper)
                    floors.add(Floor(startX, startY))
                elif column == BOX_CHAR:
                    boxes.add(Box(startX, startY))
                    floors.add(Floor(startX, startY))
                elif column == DESTINATION_CHAR:
                    destinations.add(Destination(startX, startY))
                    floors.add(Floor(startX, startY))
                elif column == 'a':
                    floors.add(Floor(startX, startY))
                startX += TILE_WIDTH
            startY += TILE_HEIGHT

    # Map center
    canvas = pygame.Surface((w * TILE_WIDTH, h * TILE_HEIGHT))
    canvasPos = canvas.get_rect(center=((WIDTH - HUD_SIZE) / 2,
                                        HEIGHT / 2))
    destinationsAmount = len(destinations.sprites())
    gamerTimer = Timer(pygame.time.get_ticks(), myFont)
    hud = HUD(gamerTimer)
    allSprites = pygame.sprite.Group(floors, walls, destinations, boxes, storekeepers)

    end = time.time()
    print(f'Set up total time: {end - start}')
    # Event loop
    while True:
        clock.tick(FPS)
        # game.check_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.playing = False
                game.check_events()
                pygame.display.update()
                game.levelMenu.monitCheckInput()
                game.display.fill(BLACK)
                game.draw_text('DO YOU WANT TO QUIT AND SAVE YOUR SCORE?', 85, midWidth, midHeight - 200, game.WHITE, game.fontName)
                game.draw_text('YES', 70, game.levelMenu.firstModuleX - 100, game.levelMenu.firstModuleY, game.WHITE, game.fontName)
                game.draw_text('NO', 70, game.levelMenu.secondModuleX + 100, game.levelMenu.secondModuleY, game.WHITE, game.fontName)

                game.levelMenu.draw_pointer()
                game.levelMenu.blit_screen()

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
                    saveBoard(w, h, allSprites, gamerTimer.passed_time)

        storekeeper.collision(walls.sprites())

        for boxSprite in boxes.sprites():
            boxesCopy = boxes.copy()
            boxesCopy.remove(boxSprite)
            storekeeper.collision_box(boxSprite)

            if storekeeper.boxCollision:
                boxSprite.move(storekeeper.direction)

                boxSprite.collision_wall(walls.sprites())
                boxSprite.collision_box(boxesCopy.sprites())

                if boxSprite.blockedByBox:
                    storekeeper.move(-storekeeper.moveX, -storekeeper.moveY)
                if boxSprite.blocked and storekeeper.direction == boxSprite.blockedDirection:
                    storekeeper.move(-storekeeper.moveX, -storekeeper.moveY)

                storekeeper.boxCollision = False

        # Check if all boxes collide with destinations
        placed_boxes = pygame.sprite.groupcollide(boxes, destinations, False, False)

        if len(placed_boxes) == destinationsAmount:
            # Correct needed stuck in lvl game
            game.currentMenu = game.mainMenu
            game.currentMenu.display_menu()
            game.gameLevel += 1
            game.gamePoints += 1
            break

        # Updating and drawing sprites groups
        storekeepers.update()
        boxes.update()

        screen.fill(BLACK)
        canvas.fill(BLACK)

        allSprites.draw(canvas)
        hud.display_timer(pygame.time.get_ticks())
        hud.display_lvl(lvlName)
        hud.display_points(points)
        hud.display_playerName(game.playerName)
        screen.blit(hud.image, hud.rect)

        screen.blit(canvas, canvasPos)
        pygame.display.update()
        pygame.display.flip()


def saveBoard(width, height, sprites, time, playerName, lvlName):
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
    :param playerName: str
        Current playing player name.
    :param lvlName: str


    :return:
        None
    """
    emptyBoard = []

    for h in range(height):
        emptyBoard.append([' '] * width)

    for sprite in sprites:
        emptyBoard[int(sprite.rect.y / TILE_HEIGHT)][int(sprite.rect.x / TILE_WIDTH)] = sprite.char

    shelfFile = shelve.open(os.path.join('./src/saves', 'test'))
    shelfFile['mainBoardVar'] = emptyBoard
    shelfFile['timeVar'] = time
    shelfFile.close()


def createMap():
    pass


def tester(screen, window):
    screen.fill(RED)
    while 1:
        window.blit(screen, (0, 0))
        pygame.display.update()
        pygame.display.flip()