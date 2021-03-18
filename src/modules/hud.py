from src.modules.settings import *


class HUD(pygame.sprite.Sprite):
    def __init__(self, timer):
        """
        Class for HUD which displays information about current game.

        :param timer:
            Timer object for time handling.
        :type timer: Timer, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((HUD_WIDTH, HUD_HEIGHT))
        self.timer = timer
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - HUD_WIDTH
        self.padding = 25

    def displayLvl(self, lvlNumber):
        """
        Display level menu on the HUD.

        :param lvlNumber:
            Full level name in convention number.txt.
        :type lvlNumber: str, required
        """
        cleanName = lvlNumber[:lvlNumber.find('.')]
        font = pygame.font.Font(None, 32)
        text = font.render(f'Level: {cleanName}', 1, WHITE)
        levelPosition = text.get_rect(y=self.padding, centerx=self.image.get_width() / 2)

        self.image.blit(text, levelPosition)

    def displayTimer(self, passedTicks):
        """
        Display passed time on the HUD.

        :param passedTicks:
            Amount of ticks that passed from the start of the game.
        :type passedTicks: int, required
        """
        self.timer.setPosition(self.image.get_width() / 2, self.padding * 2)
        self.timer.update(passedTicks)
        self.image.blit(self.timer.image, self.timer.rect)

    def displayPoints(self, passedPoints):
        """
        Display points on the HUD.

        :param passedPoints:
            Amount of points to display on the HUD.
        :type passedPoints: int, required
        """
        font = pygame.font.Font(None, 30)
        text = font.render(f'Score: {passedPoints}', 1, WHITE)
        pointsPosition = text.get_rect(y=75, centerx=self.image.get_width() / 2)
        self.image.blit(text, pointsPosition)

    def displayPlayerName(self, passedName):
        """
        Display current playing user nick name.

        :param passedName:
            Nick name to display on the HUD.
        :type passedName: str, required
        """
        font = pygame.font.Font(None, 30)
        text = font.render(f'{passedName.title()}', 1, WHITE)

        playerNamePosition = text.get_rect(y=100, centerx=self.image.get_width() / 2)

        self.image.blit(text, playerNamePosition)


class Timer(pygame.sprite.Sprite):
    def __init__(self, start, fontName):
        """
        Class which returns the time (ticks) since the game start.

        :param start:
            Start amount of ticks.
        :type start: int, required
        :param fontName:
            Name of the font.
        :type fontName: pygame.Font, required
        """
        pygame.sprite.Sprite.__init__(self)
        self.start = start
        self.passedTime = 0
        self.passedTimeStr = ''
        self.fontName = fontName
        self.x = 0
        self.y = 0
        self.buffer = 0
        self.startPause = 0
        self.endTime = 0

    def update(self, ticks):
        """
        Calculate passed time between start and current measurement.

        :param ticks:
            Current value of ticks.
        :type ticks: int, required
        """
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

        self.image = self.fontName.render(f'{self.passedTimeStr}', 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.y = self.y

    def setPosition(self, x, y):
        """
        Set position on which display Timer on the HUD.

        :param x:
            Position in x-axis.
        :type x: int, required,
        :param y:
            Position in y-axis.
        :type y: int, required
        """
        self.x = x
        self.y = y

    def stop(self, ticks):
        """
        Utility function for handling in game pause and set potential finish game
        time.

        :param ticks:
            Current value of ticks.
        :type ticks: int, required
        """
        self.startPause = ticks
        self.endTime = self.passedTime * 1000

    def resume(self, ticks):
        """
        Utility class for resume game time after in game pause.

        :param ticks:
            Current value of ticks.
        :type ticks: int, required
        """
        self.buffer += round((ticks - self.startPause) / 1000)
