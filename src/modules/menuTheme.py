from .functions import load_png
import pygame_menu

backgroundImage = pygame_menu.baseimage.BaseImage(
    image_path = 'src/img/menu_background.png',
    drawing_mode = pygame_menu.baseimage.IMAGE_MODE_CENTER
)

myTheme = pygame_menu.themes.THEME_SOLARIZED.copy()
myTheme.background_color = backgroundImage
myTheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
