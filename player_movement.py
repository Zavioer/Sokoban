import pygame, sys

# Initializes all modules, for example: time module
pygame.init()

# Variables for displaying the object
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
player_color = (255, 0, 0)
object = pygame.Rect(50, 50, 50, 50)
clock = pygame.time.Clock()
delta = 0.0

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)
        # Movement
        delta += clock.tick() / 1000.0
        while delta > 1/30.0:
            delta -= 1/30.0
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                object.x += 10
                if object.x > width - 70:
                    object.x -= 10
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                object.x -= 10
                if object.x < 20:
                    object.x += 10
            if (keys[pygame.K_w] or keys[pygame.K_UP]):
                object.y -= 10
                if object.y < 20:
                    object.y += 10
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                object.y += 10
                if object.y > height - 70:
                    object.y -= 10

    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, player_color, object)
    pygame.display.flip()