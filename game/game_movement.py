#Vytváří prostředí pro pohyb hry => sestavené tak aby jsme operace ve hře měli mimo main.py
# - Kdo je na tahu
# - Kam se můžeme hýbnout
# - Vybrání hracího kamene a další...
#Musíme potom ještě implementovat AI pro samotné hraní hry

import pygame
from datetime import datetime

from .stat_values import BLACK, SQUARE_SIZE, WHITE, GREEN, SIDEBAR_BG
from game.screen_manager import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from game.game_board import GameBoard
from game.button import Button


class Gameing:
    turn = WHITE

    def __init__(self, win):
        self._StartCall()
        self.win = win
        self.saveBtn = Button(WIDTH + 110, HEIGHT - 50, "Uložit Hru", self.SaveButtonAction)
        self.backBtn = Button(WIDTH + 140 + self.saveBtn.rect.width, HEIGHT - 50, "Hlavní Menu", self.BackButtonAction)
        self.buttons = [self.saveBtn, self.backBtn]

     #Update display, nyní jej nemusíme mít ve main.py
    def Update(self, mouse_pos):
        self.board.Draw(self.win)

        sidebar = pygame.Rect(WIDTH, 0, WINDOW_WIDTH - WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.win, SIDEBAR_BG, sidebar)

        # Update all the buttons
        for btn in self.buttons:
            btn.hover(mouse_pos)
            btn.draw(self.win)

        self.DrawCorrectMoves(self.correct_moves)
        pygame.display.update()

        # Tell main that the game should stop
        if not self.game_running:
            return False

    def _StartCall(self):
        self.selected_stone = None
        self.board = GameBoard()
        self.turn = Gameing.turn  # Tah začíná z pravidla bílí
        self.correct_moves = {}  # Ukaže možné správné pohyby pro daného hráče
        self.game_running = True  # Flag for main, doesnt actually control if game is running, that's main's job

    def GameWinner(self):
        return self.board.Winner()

    #Resetování hry do původní pozice
    def Reset(self):
       self._StartCall()

    #Metoda pro vyběr hracího kamene -> určí row a col -> hýbne s hracím kamenem dle našeho výběru
    def Select(self, row, col, pos):
        # Check if the click happened on a button
        for btn in self.buttons:
            btn.release()
            # run action for every button, end game if we get False back
            if btn.action(pos) is False:
                self.game_running = False

        # Will crash if we try to find a stone outside the game board
        if self._IsOutsideOfGameboard(pos):
            return False

        if self.selected_stone:
            result = self._Move(row, col)
            #Jestliže náš pohyb není validní tak pohyb nebude proveden a znovu zavoláme metodu Select
            if not result:
                self.selected_stone = None
                self.correct_moves = {}  # Clear the moves when piece is deselected
                self.Select(row, col, pos)

        stone = self.board.GetStone(row, col)
        #Jestliže hrací kámen který jsme vybrali existuje a vybrali jsme SVOJI barvu
        if stone != 0 and stone.color == self.turn:
            self.selected_stone = stone
            self.correct_moves = self.board.GetCorrectMoves(stone)
            self.correct_moves[(stone.row, stone.col)] = []  # Shows which piece is selected
            return True  # Výběr a pohyb je správný -> vrátíme True

        return False  # Výběr a pohyb byl nesprávný -> vrátíme False

    def ButtonClick(self, pos):
        for btn in self.buttons:
            btn.click(pos)

    # Check if mouse position (x, y) is outside of the playable area
    def _IsOutsideOfGameboard(self, pos):
        return (pos[0] < 0 or pos[1] < 0 or pos[0] > WIDTH or pos[1] > HEIGHT)

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
            # self.ChangeTurn()
        else:
            return False

        return True

    #Metoda která nám vykreslí možné správné pohyby

    def DrawCorrectMoves(self, moves):
        for move in moves:
            row, col = move
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(80)
            s.fill(GREEN)
            self.win.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Metoda pro změnu tahu
    def ChangeTurn(self):
        self.correct_moves = {}  # Odstraní zelené možnosti po našem tahu
        self.turn = BLACK if self.turn == WHITE else WHITE
        Gameing.turn = self.turn

    def SetTurn(self, color):
        self.turn = color
        Gameing.turn = self.turn

    # Button functions
    def SaveButtonAction(self):
        from game.file_manager import FileManager
        stamp = "dama-save-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        FileManager.SaveFile(self.board.GameBoard, stamp)

    def BackButtonAction(self):
        return False

    #Methods for AI

    #Method for gatting board object
    def get_board(self):
        return self.board

    #Method returns new board after AI move => updates game with new board object
    def AI_move(self, board):
        self.board = board
        self.ChangeTurn()
