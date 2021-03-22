import shelve
import math
import time
import json
from pygame.locals import *
from .blocks import Floor, Box, Destination, Wall
from .player import Player
from .hud import HUD, Timer
from .creator import Tile, Mouse, Board, Toolbox
from .game import *
from settings import *


def startTheGame(screen, lvlName, game, points, flag):
    """
    Main game logic. Handling board draw, set player. Then game loop.

    :param screen:
        Surface on which draw game.
    :type screen: pygame.Surface, required
    :param lvlName:
        Current playing game name in convention number.txt.
    :type lvlName: str, required
    :param game:
        Game object that all connection between game and menu.
    :type game: game.Game, required
    :param points:
        Number of points which game starts.
    :type points: int, required
    :param flag:
        Flag that allows to discriminate between module I, II and III.
    :type flag: str, required
    """
    start = time.time()
    myFont = pygame.font.SysFont('Montserrat', 30)

    # Initial sprites groups and map floor
    walls = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    destinations = pygame.sprite.Group()
    floors = pygame.sprite.Group()

    clock = pygame.time.Clock()

    if flag == RESTORE:
        mapWidth = game.restoreDetails['width']
        mapHeight = game.restoreDetails['height']

        startY = 0
        for rows in game.restoreDetails['emptyBoard']:
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
    else:
        # Load and place objects on the map
        if flag == MODULE_I or flag == MODULE_II:
            path = './src/boards/'
        elif flag == MODULE_III:
            path = './src/boards/own/'

        with open(os.path.join(path, lvlName), 'r') as fd:
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
    canvasPos = canvas.get_rect(center=((WIDTH - HUD_WIDTH) / 2,
                                        HEIGHT / 2))

    destinationsAmount = len(destinations.sprites())

    if flag == RESTORE:
        gamerTimer = Timer(game.restoreDetails['endTime'], myFont)
    else:
        gamerTimer = Timer(pygame.time.get_ticks(), myFont)
    hud = HUD(gamerTimer)

    allSprites = pygame.sprite.Group(floors, walls, destinations, boxes, storekeeper)

    end = time.time()
    print(f'Set up total time: {end - start}')

    # Event loop
    while game.logicState:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                game.logicState = False
                hud.timer.stop(pygame.time.get_ticks())
                game.currentMenu = game.saveGameMenu

                game.currentPlayerState['width'] = mapWidth
                game.currentPlayerState['height'] = mapHeight
                game.currentPlayerState['sprites'] = allSprites
                game.currentPlayerState['time'] = hud.timer.endTime

                game.currentMenu.displayMenu()
                hud.timer.resume(pygame.time.get_ticks())

            elif event.type == KEYDOWN:
                if event.key == K_w:
                    storekeeper.move(0, -STOREKEEPER_MOVE)
                elif event.key == K_s:
                    storekeeper.move(0, STOREKEEPER_MOVE)
                elif event.key == K_a:
                    storekeeper.move(-STOREKEEPER_MOVE, 0)
                elif event.key == K_d:
                    storekeeper.move(STOREKEEPER_MOVE, 0)
                elif event.key == K_r:
                    game.logicState = False

                    if flag == RESTORE:
                        lvlName = game.restoreDetails['lvlName']

                    resetMap(game.window, lvlName, game, game.gamePoints, flag)

        storekeeper.collision(walls.sprites())

        for boxSprite in boxes.sprites():
            boxesCopy = boxes.copy()
            boxesCopy.remove(boxSprite)
            storekeeper.collisionBox(boxSprite)

            if storekeeper.boxCollision:
                boxSprite.move(storekeeper.direction)

                boxSprite.collisionWall(walls.sprites())
                boxSprite.collisionBox(boxesCopy.sprites())

                if boxSprite.blockedByBox:
                    storekeeper.move(-storekeeper.moveX, -storekeeper.moveY)
                if boxSprite.blocked and storekeeper.direction == boxSprite.blockedDirection:
                    storekeeper.move(-storekeeper.moveX, -storekeeper.moveY)

                storekeeper.boxCollision = False

        # Check if all boxes collide with destinations
        placedBoxes = pygame.sprite.groupcollide(boxes, destinations, False, False)

        if len(placedBoxes) == destinationsAmount:
            if flag == MODULE_I or flag == MODULE_III:
                game.logicState = False
                game.currentMenu = game.mainMenu
                game.currentMenu.displayMenu()

            if flag == MODULE_II:
                game.logicState = False
                game.gameLevel += 1

                hud.timer.stop(pygame.time.get_ticks())
                score = computeScore(hud.timer.endTime)
                game.gamePoints += score
                game.START_KEY = True

        # Updating and drawing sprites groups
        storekeeper.update()
        boxes.update()

        screen.fill(BLACK)
        canvas.fill(BLACK)
        hud.image.fill(BLACK)

        allSprites.draw(canvas)

        hud.displayTimer(pygame.time.get_ticks())

        if flag == RESTORE:
            hud.displayLvl(game.restoreDetails['lvlName'])
        else:
            hud.displayLvl(lvlName)

        if flag == MODULE_II:
            hud.displayPoints(points)

        hud.displayPlayerName(game.playerName)
        screen.blit(hud.image, hud.rect)

        screen.blit(canvas, canvasPos)
        pygame.display.update()
        pygame.display.flip()


def saveBoard(width, height, sprites, endTime, playerName, lvlName, gamePoints):
    """
    Function for saving current playing lvl and additional information in to
    shelve file.

    :param width:
        Current playing board width.
    :type width: int, required
    :param height:
        Current playing map height.
    :type height: int, required
    :param sprites:
        Group of all sprites in level.
    :type sprites: pygame.sprite.Group, required
    :param endTime:
        Time in seconds passed from beginning.
    :type endTime: int, required
    :param playerName: str
        Current playing player nick name.
    :type lvlName: str, required
    """
    emptyBoard = []

    for h in range(height):
        emptyBoard.append([EMPTY_CHAR] * width)

    for sprite in sprites:
        emptyBoard[int(sprite.rect.y / TILE_HEIGHT)][int(sprite.rect.x / TILE_WIDTH)] = sprite.char

    currentDate = time.localtime(time.time())
    formatedDate = time.strftime('%H_%M_%S_%d_%m_%Y', currentDate)

    fileName = ''.join((playerName, '_', 'BOARD', '_', formatedDate))
    savesPath = os.path.abspath('../src/saves/')

    shelveFile = shelve.open(os.path.join(SAVES_DIR, fileName))

    shelveFile['widthBoardVar'] = width
    shelveFile['heightBoard'] = height
    shelveFile['lvlNameVar'] = lvlName
    shelveFile['userNameVar'] = playerName
    shelveFile['endTimeVar'] = endTime
    shelveFile['mainBoardVar'] = emptyBoard

    shelveFile.close()

    data = {
        'userNameVar': playerName,
        'userScore': gamePoints
    }

    with open('scoreFile.txt', 'a') as scoreFile:
        json.dump(data, scoreFile)
        scoreFile.write('\n')


def createMap(screen, width, height, game):
    """
    Function for module III which allows player to create own map.

    :param screen:
        Surface on which will draw canvas to draw map.
    :type screen: pygame.Surface, required
    :param width:
        Given map width. Max number 30.
    :type width: int, required
    :param height:
        Given map height. Max number 20.
    :type height: int, required
    :param game:
        Game class that allows connection between game and menu.
    :type game: game.Game, required
    """
    boardWidth = BLOCK_SIZE * width
    boardHeight = BLOCK_SIZE * height
    canvas = pygame.Surface((boardWidth, boardHeight))

    canvasCenter = canvas.get_rect(center=((screen.get_width() - TOOLBOX_WIDTH) / 2,
                                           screen.get_height() / 2))
    clock = pygame.time.Clock()

    mouse = Mouse()
    allTiles = pygame.sprite.Group()
    playerBoard = Board(width, height)
    playerBoard.emptyMap()

    toolbox = Toolbox(TOOLBOX_WIDTH, HEIGHT)

    for x in range(0, boardWidth, BLOCK_SIZE):
        pygame.draw.line(canvas, WHITE, (x, 0), (x, BOARD_WIDTH))

    for y in range(0, boardHeight, BLOCK_SIZE):
        pygame.draw.line(canvas, WHITE, (0, y), (BOARD_WIDTH, y))

    for x in range(0, boardWidth, BLOCK_SIZE):
        for y in range(0, boardHeight, BLOCK_SIZE):
            tile = Tile(x, y)

            # Map borders
            if x == 0:
                tile.setImage(WALL_IMG)
                playerBoard.placeTile(int(x / BLOCK_SIZE), int(y / BLOCK_SIZE), WALL_CHAR)
            elif x == (boardWidth - BLOCK_SIZE):
                tile.setImage(WALL_IMG)
                playerBoard.placeTile(int(x / BLOCK_SIZE), int(y / BLOCK_SIZE), WALL_CHAR)

            if y == 0:
                tile.setImage(WALL_IMG)
                playerBoard.placeTile(int(x / BLOCK_SIZE), int(y / BLOCK_SIZE), WALL_CHAR)
            elif y == (boardHeight - BLOCK_SIZE):
                tile.setImage(WALL_IMG)
                playerBoard.placeTile(int(x / BLOCK_SIZE), int(y / BLOCK_SIZE), WALL_CHAR)

            allTiles.add(tile)

    toolbox.addButton('Wall', WALL_CHAR, WALL_IMG)
    toolbox.addButton('Player', STOREKEEPER_CHAR, STOREKEEPER_IMG)
    toolbox.addButton('Box', BOX_CHAR, BOX_IMG)
    toolbox.addButton('Destination', DESTINATION_CHAR, DESTINATION_IMG)
    toolbox.addButton('Rubber / Floor', FLOOR_CHAR, FLOOR_IMG)
    toolbox.placeButtons()

    saveRect = pygame.Rect(20, 675, 160, 25)
    pygame.draw.rect(canvas, (255, 242, 88), saveRect)

    while game.logicState:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                mousex -= (WIDTH - TOOLBOX_WIDTH)

                if saveRect.collidepoint(mousex, mousey):
                    if playerBoard.checkAssets():
                        if playerBoard.destinationsEqualsBoxes():
                            playerBoard.saveBoard(game.passedMapName)
                            game.logicState = False
                            game.passedMapName = ''
                            game.currentMenu = game.mainMenu
                        else:
                            game.logicState = False
                            game.currentMenu.boxesDestinationInvalidMonit()
                            game.logicState = True
                    else:
                        game.logicState = False
                        game.currentMenu.unableToSaveMonit()
                        game.logicState = True

                for sprite in allTiles:
                    mousex, mousey = pygame.mouse.get_pos()
                    x, y = canvasCenter.topleft
                    mousex -= x
                    mousey -= y

                    if sprite.rect.collidepoint(mousex, mousey):
                        if mouse.currentImage == STOREKEEPER_IMG and not playerBoard.availablePlayer:
                            break

                        if not playerBoard.availablePlayer:
                            if sprite.character == STOREKEEPER_CHAR:
                                playerBoard.availablePlayer = True

                        sprite.setImage(mouse.currentImage)
                        sprite.character = mouse.getTile()
                        playerBoard.placeTile(int(sprite.rect.x / BLOCK_SIZE),
                                              int(sprite.rect.y / BLOCK_SIZE),
                                              mouse.getTile())

                        if mouse.currentImage == STOREKEEPER_IMG and playerBoard.availablePlayer:
                            playerBoard.availablePlayer = False

                for button in toolbox.buttonsSprites:
                    mousex, mousey = pygame.mouse.get_pos()
                    mousex -= (WIDTH - TOOLBOX_WIDTH)

                    if button.rect.collidepoint(mousex, mousey):
                        if button.tileImage == STOREKEEPER_IMG and not playerBoard.availablePlayer:
                            break

                        mouse.currentImage = button.tileImage
                        mouse.currBlock = button.attribute

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                game.runDisplay = False

        screen.fill(BLACK)
        allTiles.update()

        allTiles.draw(canvas)
        screen.blit(canvas, canvasCenter)
        screen.blit(toolbox.image, (WIDTH - TOOLBOX_WIDTH, 0))

        pygame.display.update()
        pygame.display.flip()


def resetMap(screen, lvlName, game, points, flag):
    """
    Function for reset map to default state.

    :param screen:

    :param screen:
        Surface on which draw game.
    :type screen: pygame.Surface, required
    :param lvlName:
        Current playing game name in convention number.txt.
    :type lvlName: str, required
    :param game:
        Game object that all connection between game and menu.
    :type game: game.Game, required
    :param points:
        Number of points which game starts.
    :type points: int, required
    :param flag:
        Flag that allows to discriminate between module I, II and III.
    :type flag: str, required
    """
    game.logicState = True
    startTheGame(screen, lvlName, game, points, flag)


def loadSave(fileName):
    """
    Function for restoring game detail for saves.

    :param fileName:
        Name of saved game.
    :type fileName: str, required

    :return:
        dict
    """
    savesPath = os.path.abspath('../src/saves')
    shelveFile = shelve.open(os.path.join(savesPath, fileName))
    mapDetails = {}

    mapDetails['width'] = shelveFile['widthBoardVar']
    mapDetails['height'] = shelveFile['heightBoard']
    mapDetails['lvlName'] = shelveFile['lvlNameVar']
    mapDetails['playerName'] = shelveFile['userNameVar']
    mapDetails['endTime'] = shelveFile['endTimeVar']
    mapDetails['emptyBoard'] = shelveFile['mainBoardVar']

    shelveFile.close()

    return mapDetails


def computeScore(endTicks):
    """
    Utility function to compute score result. Based on time which player finish level.

    :param endTicks:
        Amout of ticks which player needed to end a level.
    :type endTicks: int, required
    """
    if endTicks < 120000:
        return 3 * SCORE_BASE
    elif endTicks >= 120000 and  endTicks < 240000:
        return 2 * SCORE_BASE
    else:
        return SCORE_BASE
