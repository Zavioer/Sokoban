import pygame


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(0, 0, 50, 50)

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()

