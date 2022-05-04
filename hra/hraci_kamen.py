#Informace pro hrací kámen ktety bude improtován do hracího plochy

import pygame
from .hodnoty import SQUARE_SIZE

class Hraci_kamen:
    PADDING = 20 #určení velikosti hracího kamene ve prostoru 

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False #pro vytvoření hracího kamene dámy, kontrola zda jsem dáma či ne     
        self.x = 0 #x pro col
        self.y = 0 #y pro row
        self.calc_pos()

    #Metoda co určí pozici ve hracím čtverci pro vytvoření hracího kamene 
    #   Prostředek našeho místa pro hrací kámen, pro jeho správné vykreslení (Prostředek čtverce)    
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
    #Metoda co čistě jenom určí že náš hrací kámen jest nyní dáma 
    #   Můžeme použít .png obrázek korunky pro tvorbu dámy   
    def queen(self):
        self.queen = True
    
    #Metoda vykreslí hrací kámen 
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
#Potřeba stále implementovat pohyb hracího kamene (White hráč vždycky začíná jako první pokud není načteno ze partie v .csv)
#   Implementace buď ve hrací_kamenu nebo hraci_plocha nebo vlastí specifcký soubor na pohyb
#   Jak pro hráče tak pro AI
#   Binární strom pro rozhodávání správného pohybu 
#   Po stisknutí hracího kamene se zobrazí body na hrací ploše zelené barvy kam se můžeme přesunout 
#       Jinou možnost nám to nedá 