import pygame
import os
import shelve
from pygame.locals import *
from .blocks import Floor, Box, Destination, Wall
from .player import Player
from .hud import HUD, Timer
from .game import *
from .settings import *
from src.modules import menu

def start_the_game(screen, lvlName, game, points):
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
        board = fd.readlines()
        startY = 0

        for rows in board:
            startX = 0
            for column in rows:
                floors.add(Floor(startX, startY))

                if column == WALL_CHAR:
                    walls.add(Wall(startX, startY))
                elif column == STOREKEEPER_CHAR:
                    storekeeper = Player(startX, startY)
                    storekeepers.add(storekeeper)
                elif column == BOX_CHAR:
                    boxes.add(Box(startX, startY))
                elif column == DESTINATION_CHAR:
                    destinations.add(Destination(startX, startY))

                startX += TILE_WIDTH
            startY += TILE_HEIGHT

    destinationsAmount = len(destinations.sprites())
    gamerTimer = Timer(pygame.time.get_ticks(), myFont)
    hud = HUD(gamerTimer)
    allSprites = pygame.sprite.Group(walls, destinations, boxes, storekeepers)

    # Event loop
    while 1:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.check_events()
                game.playing = False
                pygame.display.update()
                game.levelMenu.monitCheckInput()
                game.display.fill((0, 0, 0))
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
                    saveBoard(22, 11, allSprites, gamerTimer.passed_time)

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

        floors.draw(screen)
        allSprites.draw(screen)
        hud.display_timer(pygame.time.get_ticks())
        hud.display_lvl(lvlName)
        hud.display_points(points)
        # hud.display_playerName(playerName)
        screen.blit(hud.image, hud.rect)

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
