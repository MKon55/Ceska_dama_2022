"""
Informace o hracím kamenu který bude importován do hracího plochy
"""

import pygame
from .stat_values import SQUARE_SIZE, CROWN


class Stone:
    """
    Třída reprezentujici herní kamen

    Attributy
    ----------
    row : int
        an Y coordinates
    col : int
        an X coordinates
    color : tuple
        barva v RGB hodnotach
    queen : bool, optional
        zda je kámen queen, či nikoliv (default = False)

    Metody
    -------
    calc_pos()
        Vypočte správné umístění a usazení hracího kamene na střed čtverce
    make_queen()
        Checkne, zda je hrací kámen dáma
        V game_board.py checkne, zda jsme na pozici, kdy se kámen může stát queen
    draw()
        Vykreslí hrací kámen na herní plochu
    move()
        Pohyb hracího kamene
    """
    PADDING = 20  # určení velikosti hracího kamene ve prostoru

    def __init__(self, row, col, color, queen=False):
        """
            Parametry
            ----------
            row : int
                an Y coordinates
            col : int
                an X coordinates
            color : tuple
                barva v RGB hodnotach
            queen : bool, optional
                zda je kámen queen, či nikoliv (default = False)
        """
        self.row = row
        self.col = col
        self.color = color
        self.queen = queen  # pro vytvoření hracího kamene dámy, kontrola zda jsem dáma či ne
        self.x = 0  # x pro col
        self.y = 0  # y pro row
        self.calc_pos()


    def calc_pos(self):
        """Vypočte správné umístění a usazení hracího kamene na střed čtverce"""
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2


    #   Můžeme použít .png obrázek korunky pro tvorbu dámy
    def make_queen(self):
        """
        Checkne, zda je hrací kámen dáma
        V game_board checkne, zda jsme na pozici, kdy se kámen může stát queen
        """
        self.queen = True


    def draw(self, win):
        """Vykreslí hrací kámen na herní plochu"""
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        #Cyklus pro vykreslení queen piece
        if self.queen:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2)) #Blit umožní vykreslení crown na hrací kámen + "matematika" pro vykreslení přímo do prostředí 
            

    def move(self, row, col):
        """Pohyb hracího kamene"""
        self.row = row
        self.col = col
        self.calc_pos() #Přepočítání aby byl kámen přesunut na prostředek čtverce 

#Potřeba stále implementovat pohyb hracího kamene (White hráč vždycky začíná jako první pokud není načteno ze partie v .csv)
#   Implementace buď ve hrací_kamenu nebo hraci_plocha nebo vlastí specifcký soubor na pohyb
#   Jak pro hráče tak pro AI
#   Binární strom pro rozhodávání správného pohybu
#   Po stisknutí hracího kamene se zobrazí body na hrací ploše zelené barvy kam se můžeme přesunout
#       Jinou možnost nám to nedá
