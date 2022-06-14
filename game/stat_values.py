#Neměné hodnoty (musíme importovat jako), Static Values
#Usnadnění práce pro rozhraní hry, samozžejmě že takto nemusíme ale příjde mi to přehlednější

import pygame
from config.localconfig import PATH

#Hodnoty
WIDTH, HEIGHT = 800, 800  # 800 x 800  hrací plocha
ROW, COL = 8, 8  # standartní
SQUARE_SIZE = WIDTH//ROW  # Velikost jednoho čtverce pro hrací kámen

#Znaky pro ukládání/načítání
WHITE_CHAR = "w"
BLACK_CHAR = "b"
WHITE_QUEEN_CHAR = "ww"
BLACK_QUEEN_CHAR = "bb"
WHITE_TURN_CHAR = "w"
BLACK_TURN_CHAR = "b"

#Barvy pro hrací kameny
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEFAULT_COLOR_TURN = WHITE

#Bude ukazovat možný pohyb po hrací ploše
GREEN = (0, 100, 0)

#Hrací pole barvy
BOARD_WHITE = (232, 208, 170)
BOARD_BLACK = (166, 125, 93)

#Načtení crown from assets + transform pro správnou velikost
CROWN = pygame.transform.scale(pygame.image.load(PATH + 'assets/crown.png'), (40, 40))
