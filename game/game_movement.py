#Vytváří prostředí pro pohyb hry => sestavené tak aby jsme operace ve hře měli mimo main.py
# - Kdo je na tahu 
# - Kam se můžeme hýbnout 
# - Vybrání hracího kamene a další...
#Musíme potom ještě implementovat AI pro samotné hraní hry

import pygame

from game.stone import Stone
from .stat_values import BLACK, SQUARE_SIZE, WHITE, GREEN
from game.game_board import Game_board

class Gameing:
    def __init__(self, win): 
        self._start_call()
        self.win = win
 
     #Update display, nyní jej nemusíme mít ve main.py
    def update(self):
        self.board.draw(self.win)
        self.draw_correct_moves(self.correct_moves)
        pygame.display.update()
           
    def _start_call(self):
        self.selected_stone = None
        self.board = Game_board()
        self.turn = WHITE #Tah začíná z pravidla bílí
        self.correct_moves = {}  #Ukaže možné správné pohyby pro daného hráče 
        
    def game_winner(self):
        return self.board.winner()
        
    #Resetování hry do původní pozice    
    def reset(self):
       self._start_call()
    
    #Metoda pro vyběr hracího kamene -> určí row a col -> hýbne s hracím kamenem dle našeho výběru 
    def select(self, row, col):
        if self.selected_stone :
            result = self._move(row, col)
            #Jestliže náš pohyb není validní tak pohyb nebude proveden a znovu zavoláme metodu select
            if not result:
                self.selected_stone = None
                self.select(row, col)
                
        stone = self.board.get_stone(row, col)
        #Jestliže hrací kámen který jsme vybrali existuje a vybrali jsme SVOJI barvu 
        if stone != 0 and stone.color == self.turn:
            self.selected_stone = stone
            self.correct_moves = self.board.get_correct_moves(stone)
            return True #Výběr a pohyb je správný -> vrátíme True 
            
        return False #Výběr a pohyb byl nesprávný -> vrátíme False 
    
    #Pro pohyb po select hracího kamene    
    def _move(self, row, col):
        stone = self.board.get_stone(row, col)
        #Jestliže platí že do vybrané pozice == 0 a je ve správném pohybu tak se hýbne 
        if self.selected_stone and stone == 0 and (row, col) in self.correct_moves:
            self.board.movement(self.selected_stone, row, col)
            skipped = self.correct_moves[(row, col)]
            #Odstranění hracího kamene ze hry pokud byl přeskočen 
            if skipped:
                self.board.remove(skipped)
            #Po provedení pohybu se změní kdo je na tahu -> call turn_change
            self.change_turn()
        else:
            return False

        return True

     
    #Metoda která nám vykreslí možné správné pohyby 
    def draw_correct_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)  
            
    #Metoda pro změnu tahu 
    def change_turn(self):
        self.correct_moves = {} #Odstraní zelené možnosti po našem tahu
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
