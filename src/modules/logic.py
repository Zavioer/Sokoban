import os
import time
import shelve
import pygame
from pygame.locals import *
from .blocks import Floor, Box, Destination, Wall
from .player import Player
from .hud import HUD, Timer
from .creator import Tile, Mouse, Board, Toolbox
from .game import *
from .settings import *


def start_the_game(screen, lvlName, game, points):
    start = time.time()
    myFont = pygame.font.SysFont('Montserrat', 30)

    # Initial sprites groups and map floor
    walls = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    destinations = pygame.sprite.Group()

    floors = pygame.sprite.Group()
    clock = pygame.time.Clock()

    # Load and place objects on the map
    with open(os.path.join('./src/boards/', lvlName), 'r') as fd:
        mapWidth = int(fd.readline())
        mapHeight = int(fd.readline())

        startY = 0
        for rows in fd:
            startX = 0
            for column in rows:
                if column == WALL_CHAR:
                    walls.add(Wall(startX, startY))
                elif column == STOREKEEPER_CHAR:
                    storekeeper = Player(startX, startY)
                    floors.add(Floor(startX, startY))
                elif column == BOX_CHAR:
                    boxes.add(Box(startX, startY))
                    floors.add(Floor(startX, startY))
                elif column == DESTINATION_CHAR:
                    destinations.add(Destination(startX, startY))
                    floors.add(Floor(startX, startY))
                elif column == FLOOR_CHAR:
                    floors.add(Floor(startX, startY))
                startX += TILE_WIDTH
            startY += TILE_HEIGHT

    # Map center
    canvas = pygame.Surface((mapWidth * TILE_WIDTH, mapHeight * TILE_HEIGHT))
    canvasPos = canvas.get_rect(center=((WIDTH - HUD_SIZE) / 2,
                                        HEIGHT / 2))

    destinationsAmount = len(destinations.sprites())
    gamerTimer = Timer(pygame.time.get_ticks(), myFont)
    hud = HUD(gamerTimer)

    allSprites = pygame.sprite.Group(floors, walls, destinations, boxes, storekeeper)

    end = time.time()
    print(f'Set up total time: {end - start}')

    # Event loop
    while game.logicState:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
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
                    saveBoard(mapWidth, mapHeight, allSprites, gamerTimer.passedTime,
                              lvlName)
                elif event.key == K_r:
                    game.logicState = False
                    resetMap(game.window, game.currentLevel, game, game.gamePoints)


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
        storekeeper.update()
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

    # while game.logicState == False:
    #     game.display.fill(BLACK)
    #     game.draw_text('DO YOU WANT TO QUIT AND SAVE YOUR SCORE?', 65, midWidth, midHeight - 300, game.WHITE, game.fontName)
    #     game.draw_text('YES', 60, game.levelMenu.firstModuleX, game.levelMenu.firstModuleY, game.WHITE, game.fontName)
    #     game.draw_text('NO', 60, game.levelMenu.secondModuleX, game.levelMenu.secondModuleY, game.WHITE, game.fontName)
    #     game.levelMenu.draw_pointer()
    #     game.levelMenu.monitCheckInput()
    #     game.levelMenu.movePointerQuit()
    #
    #     game.levelMenu.blit_screen()


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


def create_map(screen, player_name):
    canvas = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
    canvas.fill(RED)
    canvasCenter = canvas.get_rect(center=((screen.get_width() - TOOLBOX_WIDTH) / 2,
                                           screen.get_height() / 2))
    clock = pygame.time.Clock()

    mouse = Mouse()
    allTiles = pygame.sprite.Group()
    playerBoard = Board(30, 20)
    toolbox = Toolbox(TOOLBOX_WIDTH, HEIGHT)

    for x in range(0, BOARD_WIDTH, BLOCK_SIZE):
        pygame.draw.line(canvas, WHITE, (x, 0), (x, BOARD_WIDTH))

    for y in range(0, BOARD_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(canvas, WHITE, (0, y), (BOARD_WIDTH, y))

    for x in range(0, BOARD_WIDTH, BLOCK_SIZE):
        for y in range(0, BOARD_HEIGHT, BLOCK_SIZE):
            allTiles.add(Tile(x, y))

    toolbox.add_button('Wall', WALL_CHAR, WALL_IMG)
    toolbox.add_button('Player', STOREKEEPER_CHAR, STOREKEEPER_IMG)
    toolbox.add_button('Box', BOX_CHAR, BOX_IMG)
    toolbox.add_button('Destination', DESTINATION_CHAR, DESTINATION_IMG)
    # toolbox.add_button('Rubber', EMPTY_CHAR, EMPTY_IMG)
    toolbox.place_buttons()

    screen.fill(BLACK)
    playerBoard.empty_map()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                for sprite in allTiles:
                    mousex, mousey = pygame.mouse.get_pos()
                    x, y = canvasCenter.topleft
                    mousex -= x
                    mousey -= y

                    if sprite.rect.collidepoint(mousex, mousey):
                        mouse.currentImage = mouse.currentImage
                        sprite.set_image(mouse.currentImage)
                        playerBoard.place_tile(int(sprite.rect.x / BLOCK_SIZE),
                                               int(sprite.rect.y / BLOCK_SIZE),
                                               mouse.get_tile())

                for button in toolbox.buttonsSprites:
                    mousex, mousey = pygame.mouse.get_pos()
                    mousex -= (WIDTH - TOOLBOX_WIDTH)

                    if button.rect.collidepoint(mousex, mousey):
                        mouse.currentImage = button.tileImage
                        mouse.currBlock = button.attribute

            elif event.type == KEYDOWN and event.key == K_s:
                playerBoard.save_board()

        screen.blit(canvas, canvasCenter)
        allTiles.update()
        allTiles.draw(canvas)
        screen.blit(toolbox.image, (WIDTH - 200, 0))

        pygame.display.update()
        pygame.display.flip()

def resetMap(screen, lvlName, game, points):
    game.logicState = True
    start_the_game(screen, lvlName, game, points)