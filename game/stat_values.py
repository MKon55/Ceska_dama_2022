# Neměné hodnoty (musíme importovat jako), Static Values
# Usnadnění práce pro rozhraní hry, samozžejmě že takto nemusíme ale příjde mi to přehlednější

import pygame
import pygame_menu

from config.localconfig import PATH
from game.screen_manager import WIDTH, WINDOW_WIDTH

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

# Color Theme
BACKGROUND = (193, 193, 197)
UI_HIGHLIGHT = (198, 25, 44)
UI_LIGHT = (240, 240, 240)
UI_NORMAL = (167, 167, 171)
UI_DARK = (130, 130, 133)
UI_DARKER = (67, 67, 69)
UI_DARKEST = (14, 14, 14)


# Barvy pro hrací kameny
WHITE = (198, 25, 44)
BLACK = (24, 14, 14)
DEFAULT_COLOR_TURN = WHITE

# Localization
WHITE_TEXT = "Červená"
BLACK_TEXT = "Černá  "

# Bude ukazovat možný pohyb po hrací ploše
GREEN = (112, 250, 7)
LAST_TURN = (6, 136, 199)

# Hrací pole barvy
BOARD_WHITE = (222, 222, 227)
BOARD_BLACK = (163, 163, 167)

# UI colors
SIDEBAR_BG = BACKGROUND
BUTTON_BG = UI_NORMAL
BUTTON_TEXT = UI_DARKER
BUTTON_HOVER = UI_DARK
BUTTON_HOVER_TEXT = UI_DARKER
BUTTON_PRESS = UI_DARKER
BUTTON_PRESS_TEXT = UI_DARKEST

# Načtení crown from assets + transform pro správnou velikost
CROWN = pygame.transform.scale(pygame.image.load(PATH + 'assets/crown.png'), (40, 40))

# Main menu Theme
MENUTHEME = pygame_menu.Theme(
    background_color=BACKGROUND,
    title_background_color=BACKGROUND,
    title_font_shadow=False,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    title_font_color=UI_HIGHLIGHT,
    title_font_size=150,
    title_offset=(WINDOW_WIDTH / 2 - 200, 50),
    # title_offset=(WIDTH / 2, 0),
    widget_padding=25,
    title_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
    widget_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
    selection_color=UI_HIGHLIGHT
)
