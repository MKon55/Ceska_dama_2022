# Vytváří hrací plochu pro dámu
# Pohyb hracích kamenů

import pygame
# musí být . jinak neví že .py je ve stejné složce
from .stat_values import BOARD_BLACK, BOARD_WHITE, SQUARE_SIZE, ROW, COL, BLACK, WHITE
from .stone import Stone


class Game_board:
    def __init__(self):
        self._game_board = []
        self.black_left = self.white_left = 12
        self.black_queens = self.white_queens = 0
        self.create_game_board()

    # Metody vytvoří herní plochu
    def create_game_board(self):
        for row in range(ROW):
            self._game_board.append([])  # List pro každou řadu
            for col in range(COL):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self._game_board[row].append(
                            Stone(row, col, BLACK))
                    elif row > 4:
                        self._game_board[row].append(
                            Stone(row, col, WHITE))
                    else:  # Jestliže na místě není hrací kámen tak 0
                        self._game_board[row].append(0)
                else:
                    self._game_board[row].append(0)

    #Metoda pro načtení hrací plochy
    def load_board(self, board):  # Format: [['a1', 'w'], ['c1', 'w'], ['e1', 'ww']m ... ['b4', 'b']]
        self.clear_board()

        for stone in board:
            notation = stone[0]
            color_and_queen = stone[1]

            position = Game_board.notation_to_coordinates(notation)
            row = position[0]
            col = position[1]

            if color_and_queen == "b":
                self._game_board[row][col] = Stone(row, col, BLACK, False)
            elif color_and_queen == "bb":
                self._game_board[row][col] = Stone(row, col, BLACK, True)
            elif color_and_queen == "w":
                self._game_board[row][col] = Stone(row, col, WHITE, False)
            elif color_and_queen == "ww":
                self._game_board[row][col] = Stone(row, col, WHITE, True)

    #Vyčištení hrací plochy
    def clear_board(self):
        self._game_board = []
        for row in range(ROW):
            self._game_board.append([])
            for col in range(COL):
                self._game_board[row].append(0)

    # Metoda vykreslí hrací kameny a hrací pole => hrací plochu
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROW):
            for col in range(COL):
                piece = self._game_board[row][col]
                if piece != 0:
                    piece.draw(win)

    # Metoda vykreslí čtverce ve kterých budou hrací kameny
    def draw_squares(self, win):
        win.fill(BOARD_BLACK)
        for row in range(ROW):
            # step 2 pro správné vykreslení (střídání 2 steps a 1 step)
            for col in range(row % 2, COL, 2):
                # topleft = 0,0 (x směrem do prava a y směrem dolu )
                pygame.draw.rect(win, BOARD_WHITE, (row*SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    #Metoda pro pohyb
    #1. pohyb kamene v listu + 2. update 
    def movement(self, stone, row, col):
        # Prohození pozic hodnot; nemusíme vytvářet temp
        self.game_board[stone.row][stone.col], self.game_board[row][col] = self.game_board[row][col], self.game_board[stone.row][stone.col]
        stone.movement(row, col)
        
        #Kontrola zda jsme na pozici kdy se stone může stát queen + update hodnot self.black_queens a self.white_queens 
        if row == ROW or row == 0: #Jestliže jsme na pozici 0 nebo 7 tak jsme na konci či začátku hrací plohcy => kámen se stává dámou 
            stone.make_queen()
            if stone.color == BLACK:
                self.black_queens += 1
            else: 
                self.white_queens += 1
       
    #Metoda pro stone aby jsme jej mohli předat do movement v main()         
    def get_stone(self, row, col):
        return self.game_board[row][col]

    @property
    def game_board(self):
        return self._game_board

    @game_board.setter
    def game_board(self, value):
        self._game_board = value

    @game_board.deleter
    def game_board(self):
        del self._game_board

    @staticmethod
    def notation_to_coordinates(notation):
        letters = [char for char in "abcdefghijklmnopqrstuvwxyz"]
        split = [c for c in notation]
        return [ROW - int(split[1]), letters.index(split[0])]

    @staticmethod
    def coordinates_to_notation(row, col):
        letters = [char for char in "abcdefghijklmnopqrstuvwxyz"]
        return f"{letters[col]}{ROW - row}"

    @staticmethod
    def is_black_tile(tile_notation):
        coordinates = Game_board.notation_to_coordinates(tile_notation)
        row = coordinates[0]
        col = coordinates[1]
        if row % 2 == 0:  # Odd rows - black tiles are on odd cols
            if col % 2 == 1:
                return True
        else:  # Even rows - black tiles are on even cols
            if col % 2 == 0:
                return True
        return False
