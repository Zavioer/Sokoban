import pygame
from src.modules.board_class import Board


def main():
    # Initialize PyGame
    pygame.init()
    screen = pygame.display.set_mode((500, 500))

    # Set up images for draw
    wall = pygame.image.load('src/img/wall.png')
    player = pygame.image.load('src/img/player.png')
    floor = pygame.image.load('src/img/flor.png')
    box = pygame.image.load('src/img/box.png')
    dest = pygame.image.load('src/img/dest.png')

    board = Board( screen)
    board.load_map('src/boards/1.txt')

    board.draw_map(50, 50, player, wall, box, dest, floor)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
    main()
