from .functions import load_png
from src.modules import logic
import pygame_menu

backgroundImage = pygame_menu.baseimage.BaseImage(
    image_path = 'src/img/menu_background.png',
    drawing_mode = pygame_menu.baseimage.IMAGE_MODE_CENTER
)

myTheme = pygame_menu.themes.THEME_SOLARIZED.copy()
myTheme.background_color = backgroundImage
myTheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

# Initialize screen
def draw_menu(screen):
    menu = pygame_menu.Menu(720, 1280, 'SOKOBAN 1.0.0', theme=pygame_menu.themes.THEME_SOLARIZED)
    name = menu.add_text_input('NAME: ', default='')
    menu.add_button('PLAY', logic.start_the_game, screen, '61.txt')
    menu.add_button('QUIT', pygame_menu.events.EXIT)
    menu.add_button('CHOOSE LEVEL', pygame_menu.events.EXIT)
    menu.mainloop(screen)
