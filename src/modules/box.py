import pygame
from .functions import load_png

class Box(pygame.sprite.Sprite):
    """
    A box that will move across the screen moved by a warehouse worker
    Returns: box objects
    Functions: update, collision, collision_wall, reach, move
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('box.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.x = x
        self.rect.y = y
        self.moveable = True
        self.rect.height = 50
        self.rect.width = 50
        self.lastmove = ''

    def update(self):
        pass

    def collision(self, player, direction):
        if self.rect.colliderect(player):
            self.move(direction)
            self.lastmove = direction

    def collision_wall(self, object_list, direction):
        if self.rect.collidelist(object_list) != -1:
            self.moveable = False
            self.move('back'+self.lastmove)

        else:
            self.moveable = True

    # def reach(self, destination, background):
    #     if self.rect.collidelist(destination) != -1:
    #         font = pygame.font.Font(None, 36)
    #         text = font.render("Win!", 1, (10, 10, 10))
    #         textpos = text.get_rect()
    #         textpos.centerx = background.get_rect().centerx
    #         background.blit(text, textpos)

    def move(self, direction):
        if self.moveable:
            if direction == 'north':
                self.rect.y -= 50
            elif direction == 'south':
                self.rect.y += 50
            elif direction == 'east':
                self.rect.x += 50
            elif direction == 'west':
                self.rect.x -= 50
        else:
            if direction == 'backnorth':
                self.rect.y += 50
            elif direction == 'backsouth':
                self.rect.y -= 50
            elif direction == 'backeast':
                self.rect.x -= 50
            elif direction == 'backwest':
                self.rect.x += 50
