import pygame


class Board:
    """
    Class for single Sokoban board.

    Parameters
    ----------
    screen: pygame.Screen, required
        Pygame Screen object to draw on.
    """
    board_map = [[]]
    i = 0

    def __init__(self, screen: "pygame.display.set_mode()"):
        self.screen = screen

    def load_map(self, board_path: str):
        """
        Load map form file. Map is .txt file with convention:
        $ - player
        . - floor
        # - wall
        * - box destination field
        + - box

        :param
        board_path: file_path, required
            Path to location with map saved in .txt format.
        """
        with open(board_path, 'r') as f:
            for line in f:
                self.board_map.append([])
                for char in line:
                    self.board_map[self.i].append(char)

                self.i += 1

    def draw_map(self, object_width: float, object_height: float, player: str,
                 wall: str, box: str, dest: str, floor: str):
        """
        Draw loaded map on Screen object given in constructor.

        :param
        object_width: float, required
            Width of loaded rect object.
        :param
        object_height: float, required
            Height of loaded rect object.
        :param
        player: str, required
            Path to image with player object.
        :param
        wall: str, required
            Path to image with wall object.
        :param
        box: str, required
            Path to image with box object.
        :param
        dest: str, required
            Path to image with box destination object.
        :param
        floor: str, required
            Path to image with floor object.
        """
        start_x = 0
        start_y = 0

        for rows in self.board_map:
            start_x = 0
            for column in rows:

                if column == '#':
                    self.screen.blit(wall, (start_x, start_y))
                elif column == '$':
                    self.screen.blit(player, (start_x, start_y))
                elif column == '+':
                    self.screen.blit(box, (start_x, start_y))
                elif column == '*':
                    self.screen.blit(dest, (start_x, start_y))
                elif column == '.':
                    self.screen.blit(floor, (start_x, start_y))

                start_x += object_width
            start_y += object_height

        pygame.display.flip()
