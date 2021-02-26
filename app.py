#!/usr/bin/python
#
# Sokoban
# A simple game with realistic physics and AI
# Released as a part of the Motorola 2020 competition


from src.modules.game import Game


def main():
    game = Game()
    while game.running:
        game.curr_menu.display_menu()
        game.game_loop()


if __name__ == '__main__':
    main()