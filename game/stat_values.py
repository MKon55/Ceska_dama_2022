#Neměné hodnoty (musíme importovat jako), Static Values
#Usnadnění práce pro rozhraní hry, samozžejmě že takto nemusíme ale příjde mi to přehlednější

import pygame
from config.localconfig import PATH
from screeninfo import get_monitors
WIDTH, HEIGHT = 0, 0

#Tato metoda nastaví dynamickou velikost plochy
def GetAndSetScreenSize():
    global HEIGHT
    global WIDTH
    for m in get_monitors():
        if(m.is_primary == True):
            WIDTH = m.width//2
            HEIGHT = WIDTH
GetAndSetScreenSize()

#Hodnoty
ROW, COL = 8, 8  # standartní
SQUARE_SIZE = WIDTH//ROW  # Velikost jednoho čtverce pro hrací kámen

#Barvy pro hrací kameny
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Bude ukazovat možný pohyb po hrací ploše
GREEN = (0, 100, 0)

#Hrací pole barvy
BOARD_WHITE = (232, 208, 170)
BOARD_BLACK = (166, 125, 93)

#Načtení crown from assets + transform pro správnou velikost
CROWN = pygame.transform.scale(pygame.image.load(PATH + 'assets/crown3.png'), (40, 30))

