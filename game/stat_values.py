# Neměné hodnoty (musíme importovat jako), Static Values
# Usnadnění práce pro rozhraní hry, samozžejmě že takto nemusíme ale příjde mi to přehlednější

import pygame
import pygame_menu

from config.localconfig import PATH
from game.screen_manager import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT

# Hodnoty
ROW, COL = 8, 8  # standartní
SQUARE_SIZE = WIDTH//ROW  # Velikost jednoho čtverce pro hrací kámen

# Znaky pro ukládání/načítání
WHITE_CHAR = "w"
BLACK_CHAR = "b"
WHITE_QUEEN_CHAR = "ww"
BLACK_QUEEN_CHAR = "bb"
WHITE_TURN_CHAR = "w"
BLACK_TURN_CHAR = "b"

# Barvy pro hrací kameny
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEFAULT_COLOR_TURN = WHITE

# Bude ukazovat možný pohyb po hrací ploše
GREEN = (0, 100, 0)

# Hrací pole barvy
BOARD_WHITE = (232, 208, 170)
BOARD_BLACK = (166, 125, 93)

# Other colors
SIDEBAR_BG = (204, 255, 224)
BUTTON_BG = (184, 230, 202)
BUTTON_TEXT = (51, 64, 56)
BUTTON_HOVER = (102, 128, 112)
BUTTON_HOVER_TEXT = (51, 64, 56)
BUTTON_PRESS = (51, 64, 56)
BUTTON_PRESS_TEXT = (0, 0, 0)

# Načtení crown from assets + transform pro správnou velikost
CROWN = pygame.transform.scale(pygame.image.load(PATH + 'assets/crown.png'), (40, 40))

# Main menu Theme
MENUTHEME = pygame_menu.Theme(
    background_color=(204, 255, 224),
    title_background_color=(25, 200, 25),
    title_font_shadow=False,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    title_font_color=(14, 14, 14),
    title_font_size=150,
    title_offset=(WINDOW_WIDTH / 2 - 200, 50),
    # title_offset=(WIDTH / 2, 0),
    widget_padding=25,
    title_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
    widget_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
    selection_color=(15, 200, 15)
)
