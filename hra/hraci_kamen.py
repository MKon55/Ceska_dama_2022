#Informace pro hrací kámen ktety bude improtován do hracího plochy

import pygame
from .hodnoty import SQUARE_SIZE

class Hraci_kamen:
    PADDING = 20

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False #pro vytvoření hracího kamene dámy, kontrola zda jsem dáma či ne     
        self.x = 0 #x pro col
        self.y = 0 #y pro row
        self.calc_pos()

    #Metoda co určí pozici ve hracím čtverci pro vytvoření hracího kamene 
    #Prostředek našeho místo pro hrací kámen, pro jeho správné vykreslení    
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
    #Metoda co čistě jenom určí že náš hrací kámen jest nyní dáma   
    def make_king(self):
        self.king = True
    
    #Metoda vykreslí hrací kámen 
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)