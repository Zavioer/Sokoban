import pygame
import math
from .settings import *


class HUD(pygame.sprite.Sprite):
    """
    Class for HUD which displays information about current game.
    """
    def __init__(self, timer):
        """
        :param timer: Timer
            Timer object for time handling.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((HUD_SIZE, WIDTH))
        self.image.fill(RED)
        self.timer = timer
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - HUD_SIZE
        self.padding = 25

    def display_lvl(self, lvl_number):
        cleanName = lvl_number[:lvl_number.find('.')]
        font = pygame.font.Font(None, 32)
        text = font.render(f'Level number: {cleanName}', 1, WHITE)
        levelPosition = text.get_rect(y = self.padding, centerx= self.image.get_width() / 2)
        self.image.blit(text, levelPosition)

    def display_timer(self, passedTicks):
        self.image.fill(RED)
        self.timer.set_position(self.image.get_width() / 2, self.padding * 2)
        self.timer.update(passedTicks)
        self.image.blit(self.timer.image, self.timer.rect)

    def display_points(self, passedPoints):
        font = pygame.font.Font(None, 30)
        text = font.render(f'Points: {passedPoints}', 1, WHITE)
        pointsPosition = text.get_rect(y = 75, centerx= self.image.get_width() / 2)
        self.image.blit(text, pointsPosition)

    def display_playerName(self, passedName):
        font = pygame.font.Font(None, 30)
        text = font.render(f'Nick: {passedName}', 1, WHITE)

        playerNamePosition = text.get_rect(y = 100, centerx=self.image.get_width() / 2)

        self.image.blit(text, playerNamePosition)


class Timer(pygame.sprite.Sprite):
    """
        Class which returns the time (ticks) since the game-start
    """
    def __init__(self, start, fontName):
        pygame.sprite.Sprite.__init__(self)
        self.start = start
        self.passedTime = 0
        self.passedTimeStr = ''
        self.fontName = fontName
        self.x = 0
        self.y = 0
        self.buffer = 0
        self.startPause = 0
        self.end_time = 0

    def update(self, ticks):
        self.passedTime = round((ticks - self.start) / 1000)

        if self.buffer > 0:
            self.passedTime -= self.buffer

        minutes = int(self.passedTime / 60)
        seconds = int(self.passedTime % 60)

        if minutes < 10:
            minutes = "0" + str(minutes)
        elif minutes > 60:
            hours = int(self.passedTime / 3600)
            if hours < 10:
                hours = "0" + str(hours)
            self.passedTimeStr = str(hours) + ":" + str(minutes) + ":" + str(seconds)
        if seconds < 10:
            seconds = "0" + str(seconds)
        self.passedTimeStr = str(minutes) + ":" + str(seconds)

        self.image = self.fontName.render(f'Time: {self.passedTimeStr}', 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.y = self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def stop(self, ticks):
        self.startPause = ticks
        self.end_time = self.passedTime * 1000

    def resume(self, ticks):
        self.buffer += round((ticks - self.startPause) / 1000)
