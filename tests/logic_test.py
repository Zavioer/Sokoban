import unittest
import os
import pygame
from pathlib import Path
from modules.logic import saveBoard, loadSave
from settings import TILE_WIDTH, TILE_HEIGHT


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([TILE_WIDTH, TILE_HEIGHT])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.char = 'X'


class SaveBoardLogicTestCase(unittest.TestCase):
    def setUp(self):
        self.path = Path(os.path.abspath('../src/saves/'))
        self.basicSprite = BasicSprite
        self.width = 5
        self.height = 5
        self.allSprites = pygame.sprite.Group()
        self.endTime = 0
        self.playerName = 'user'
        self.lvlName = 1
        self.gamePoints = 0
        self.board = []

        for h in range(self.height):
            self.board.append([' '] * self.width)

        for y in range(self.height):
            for x in range(self.width):
                sprite = self.basicSprite(x * TILE_WIDTH, y * TILE_HEIGHT)
                self.allSprites.add(sprite)
                self.board[x][y] = sprite.char

    def test_01__check_if_board_save_working(self):
        saved = False

        saveBoard(self.width, self.height, self.allSprites, self.endTime, self.playerName,
                  self.lvlName, self.gamePoints)

        saves = os.listdir(self.path)

        for save in saves:
            if save.find(self.playerName) > -1:
                saved = True
                break

        self.assertTrue(saved, 'Did not save map correctly.')

        print('> (test_01) saveBoard function correctly saves board to shelve file.')

    def test_02__check_if_data_saved_correctly(self):
        saves = os.listdir(self.path)
        fileName = ''

        for save in saves:
            if save.find(self.playerName) > -1:
                fileName = save
                break

        fileName = fileName[:len(fileName) - 4]

        results = loadSave(fileName)

        self.assertEqual(self.width, results['width'], 'Width parameters is wrong!')
        self.assertEqual(self.height, results['height'], 'Height parameters is wrong!')
        self.assertEqual(self.lvlName, results['lvlName'], 'LvlName parameters is wrong!')
        self.assertEqual(self.playerName, results['playerName'], 'PlayerName parameters is wrong!')
        self.assertEqual(self.endTime, results['endTime'], 'EndTime parameters is wrong!')
        self.assertEqual(self.board, results['emptyBoard'], 'EmptyBoard parameters is wrong!')

        print('> (test_02) All parameters were saved correctly.')


if __name__ == '__main__':
    unittest.main()
