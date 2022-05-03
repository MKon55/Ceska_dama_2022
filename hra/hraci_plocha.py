#Vytváří hrací plochu pro dámu 
#Pohyb hracích kamenů 

import pygame
from .hodnoty import BOARD_BLACK, BOARD_WHITE, SQUARE_SIZE, ROW, COL, BLACK, WHITE #musí být . jinak neví že .py je ve stejné složce 
from .hraci_kamen import Hraci_kamen

class Hraci_plocha:
    def __init__(self):
        self.herni_plocha = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.vytvoreni_herni_plochy()
        
    #Metoda vykreslí čtverce ve kterých budou hrací kameny   
    def draw_squares(self, win):
        win.fill(BOARD_BLACK)
        for row in range(ROW):
            for col in range(row % 2, COL, 2): #step 2 pro správné vykreslení (střídání 2 steps a 1 step)
                pygame.draw.rect(win, BOARD_WHITE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) #topleft = 0,0 (x směrem do prava a y směrem dolu )
                
    #Metody vytvoří herní plochu             
    def vytvoreni_herni_plochy(self):
        for row in range(ROW):
            self.herni_plocha.append([]) #List pro každou řadu
            for col in range(COL):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.herni_plocha[row].append(Hraci_kamen(row, col, BLACK))
                    elif row > 4:
                        self.herni_plocha[row].append(Hraci_kamen(row, col, WHITE))
                    else:
                        self.herni_plocha[row].append(0) #Jestliže na místě není hrací kámen tak 0 
                else:
                    self.herni_plocha[row].append(0)
    #Metoda vykreslí hrací kameny a hrací pole => hrací plochu    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROW):
            for col in range(COL):
                piece = self.herni_plocha[row][col]
                if piece != 0:
                    piece.draw(win)