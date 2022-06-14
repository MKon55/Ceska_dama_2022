#Vytváří prostředí pro pohyb hry => sestavené tak aby jsme operace ve hře měli mimo main.py
# - Kdo je na tahu
# - Kam se můžeme hýbnout
# - Vybrání hracího kamene a další...
#Musíme potom ještě implementovat AI pro samotné hraní hry

import pygame

from game.stone import Stone
from .stat_values import BLACK, SQUARE_SIZE, WHITE, GREEN
from game.game_board import GameBoard


class Gameing:
    turn = WHITE

    def __init__(self, win):
        self._StartCall()
        self.win = win

     #Update display, nyní jej nemusíme mít ve main.py
    def Update(self):
        self.board.Draw(self.win)
        self.DrawCorrectMoves(self.correct_moves)
        pygame.display.update()

    def _StartCall(self):
        self.selected_stone = None
        self.board = GameBoard()
        self.turn = Gameing.turn  # Tah začíná z pravidla bílí
        self.correct_moves = {}  # Ukaže možné správné pohyby pro daného hráče

    def GameWinner(self):
        return self.board.Winner()

    #Resetování hry do původní pozice
    def Reset(self):
       self._StartCall()

    #Metoda pro vyběr hracího kamene -> určí row a col -> hýbne s hracím kamenem dle našeho výběru
    def Select(self, row, col):
        if self.selected_stone:
            result = self._Move(row, col)
            #Jestliže náš pohyb není validní tak pohyb nebude proveden a znovu zavoláme metodu Select
            if not result:
                self.selected_stone = None
                self.Select(row, col)

        stone = self.board.GetStone(row, col)
        #Jestliže hrací kámen který jsme vybrali existuje a vybrali jsme SVOJI barvu
        if stone != 0 and stone.color == self.turn:
            self.selected_stone = stone
            self.correct_moves = self.board.GetCorrectMoves(stone)
            return True  # Výběr a pohyb je správný -> vrátíme True

        return False  # Výběr a pohyb byl nesprávný -> vrátíme False

    #Pro pohyb po Select hracího kamene
    def _Move(self, row, col):
        stone = self.board.GetStone(row, col)
        #Jestliže platí že do vybrané pozice == 0 a je ve správném pohybu tak se hýbne
        if self.selected_stone and stone == 0 and (row, col) in self.correct_moves:
            self.board.Movement(self.selected_stone, row, col)
            skipped = self.correct_moves[(row, col)]
            #Odstranění hracího kamene ze hry pokud byl přeskočen
            if skipped:
                self.board.Remove(skipped)
            #Po provedení pohybu se změní kdo je na tahu -> call turn_change
            self.ChangeTurn()
        else:
            return False

        return True

    #Metoda která nám vykreslí možné správné pohyby

    def DrawCorrectMoves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    #Metoda pro změnu tahu
    def ChangeTurn(self):
        self.correct_moves = {}  # Odstraní zelené možnosti po našem tahu
        self.turn = BLACK if self.turn == WHITE else WHITE
        Gameing.turn = self.turn
        # if self.turn == WHITE:
        #     self.turn = BLACK
        # else:
        #     self.turn = WHITE

    def SetTurn(self, color):
        self.turn = color
        Gameing.turn = self.turn
