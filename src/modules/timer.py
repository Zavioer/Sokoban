import pygame
import os
"""
    Class which returns the time (ticks) since the game-start
"""
class Timer():
    def __init__(self):
        self._start = 0
    def start(self):
        self._start = pygame.time.get_ticks()
    def current(self):
        return (pygame.time.get_ticks() - self._start)
