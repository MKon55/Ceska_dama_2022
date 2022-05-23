# Vytváří hrací plochu pro dámu
# Pohyb hracích kamenů

import pygame
# musí být . jinak neví že .py je ve stejné složce
from .hodnoty import BOARD_BLACK, BOARD_WHITE, SQUARE_SIZE, ROW, COL, BLACK, WHITE
from .hraci_kamen import Hraci_kamen


class Hraci_plocha:
    def __init__(self):
        self._herni_plocha = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.vytvoreni_herni_plochy()

    # Metody vytvoří herní plochu
    def vytvoreni_herni_plochy(self):
        for row in range(ROW):
            self._herni_plocha.append([])  # List pro každou řadu
            for col in range(COL):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self._herni_plocha[row].append(
                            Hraci_kamen(row, col, BLACK))
                    elif row > 4:
                        self._herni_plocha[row].append(
                            Hraci_kamen(row, col, WHITE))
                    else:  # Jestliže na místě není hrací kámen tak 0
                        self._herni_plocha[row].append(0)
                else:
                    self._herni_plocha[row].append(0)

    # Metoda vykreslí hrací kameny a hrací pole => hrací plochu
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROW):
            for col in range(COL):
                piece = self._herni_plocha[row][col]
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

    @property
    def herni_plocha(self):
        return self._herni_plocha

    @herni_plocha.setter
    def herni_plocha(self, value):
        self._herni_plocha = value

    @herni_plocha.deleter
    def herni_plocha(self):
        del self._herni_plocha

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
        coordinates = Hraci_plocha.notation_to_coordinates(tile_notation)
        row = coordinates[0]
        col = coordinates[1]
        if row % 2 == 0:  # Odd rows - black tiles are on odd cols
            if col % 2 == 1:
                return True
        else:  # Even rows - black tiles are on even cols
            if col % 2 == 0:
                return True
        return False
