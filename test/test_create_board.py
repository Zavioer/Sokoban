import unittest
from modules import creator
from settings import *


class CreateBoardTestCase(unittest.TestCase):
    def setUp(self):
        self.width = 5
        self.height = 5
        self.board = creator.Board(self.width, self.height)
        self.board.emptyMap()

    def test_01__check_if_correctly_check_all_assets(self):
        # Placing all needed objects in map
        self.board.placeTile(0, 1, STOREKEEPER_CHAR)
        self.board.placeTile(1, 1, WALL_CHAR)
        self.board.placeTile(2, 1, BOX_CHAR)
        self.board.placeTile(3, 1, DESTINATION_CHAR)
        self.board.placeTile(4, 1, FLOOR_CHAR)

        result = self.board.checkAssets()

        self.assertTrue(result, 'Method checkAssets incorrect check if all objects'
                                'were placed on the map.')

        print('> (test 1) Method correctly check if all objects were placed on the'
              ' map.')

    def test_02__check_if_correctly_check_all_assets_not_placed(self):
        # Placing all needed objects in map
        self.board.emptyMap()

        result = self.board.checkAssets()

        self.assertFalse(result, 'Method return true but not all assets were placed.')

        print('> (test 2) Method correctly return False if not all assets were placed'
              ' on the map.')

    def test_03__check_if_destination_amounts_equals_boxes_amount(self):
        # Placing all needed objects in map
        self.board.emptyMap()
        self.board.placeTile(0, 1, BOX_CHAR)
        self.board.placeTile(1, 1, DESTINATION_CHAR)

        result = self.board.destinationsEqualsBoxes()

        self.assertTrue(result, 'Method return False but boxes amount is less then'
                                ' destination amount.')

        print('> (test 3) Method correctly check if boxes amount is not less then'
              ' destination amount.')

    def test_04__check_if_method_for_checking_boxes_and_destination_amount_return_correctly_false(self):
        # Placing all needed objects in map
        self.board.emptyMap()
        self.board.placeTile(1, 1, DESTINATION_CHAR)

        result = self.board.destinationsEqualsBoxes()

        self.assertFalse(result, 'Method return True but boxes amount is less then'
                                 ' destinations amount.')

        print('> (test 4) Method correctly return False if boxes amount is less then'
              ' destinations amount.')

    def test_05__check_if_boxes_amount_can_be_greater_than_destinations_amount(self):
        self.board.emptyMap()
        self.board.placeTile(0, 1, BOX_CHAR)
        self.board.placeTile(0, 2, BOX_CHAR)
        self.board.placeTile(1, 1, DESTINATION_CHAR)

        result = self.board.destinationsEqualsBoxes()

        self.assertTrue(result, 'Method return False if boxes amount is greater'
                                'than destinations amount.')

        print('> (test 5) Method correctly allows situation when boxes amount is'
              ' greater than destinations amount.')


if __name__ == '__main__':
    unittest.main()
