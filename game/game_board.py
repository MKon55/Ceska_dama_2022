# Vytváří hrací plochu pro dámu
# Pohyb hracích kamenů

import pygame
# musí být . jinak neví že .py je ve stejné složce
from .stat_values import BOARD_BLACK, BOARD_WHITE, SQUARE_SIZE, ROW, COL, BLACK, WHITE
from .piece_normal import PieceNormal
from .piece_queen import PieceQueen


class GameBoard:
    def __init__(self):
        self._GameBoard = []
        self.black_left = 12
        self.white_left = 12
        self.black_queens = 0
        self.white_queens = 0
        self.forcedMoves = {}
        self.CreateGameBoard()

    # Metoda vytvoří herní plochu
    def CreateGameBoard(self):
        for row in range(ROW):
            self._GameBoard.append([])  # List pro každou řadu
            for col in range(COL):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self._GameBoard[row].append(
                            PieceNormal(row, col, BLACK))
                    elif row > 4:
                        self._GameBoard[row].append(
                            PieceNormal(row, col, WHITE))
                    else:  # Jestliže na místě není hrací kámen tak 0
                        self._GameBoard[row].append(0)
                else:
                    self._GameBoard[row].append(0)

    #Metoda pro načtení hrací plochy
    def LoadBoard(self, board):  # Format: [['a1', 'w'], ['c1', 'w'], ['e1', 'ww']m ... ['b4', 'b']]
        self.ClearBoard()

        for stone in board:
            notation = stone[0]
            color_and_queen = stone[1]

            position = GameBoard.NotationToCoordinates(notation)
            row = position[0]
            col = position[1]

            if color_and_queen == "b":
                self._GameBoard[row][col] = PieceNormal(row, col, BLACK)
            elif color_and_queen == "bb":
                self._GameBoard[row][col] = PieceQueen(row, col, BLACK)
            elif color_and_queen == "w":
                self._GameBoard[row][col] = PieceNormal(row, col, WHITE)
            elif color_and_queen == "ww":
                self._GameBoard[row][col] = PieceQueen(row, col, WHITE)

    #Vyčištení hrací plochy
    def ClearBoard(self):
        self._GameBoard = []
        for row in range(ROW):
            self._GameBoard.append([])
            for col in range(COL):
                self._GameBoard[row].append(0)

    # Metoda vykreslí čtverce ve kterých budou hrací kameny
    def DrawSquares(self, win):
        win.fill(BOARD_BLACK)
        for row in range(ROW):
            # step 2 pro správné vykreslení (střídání 2 steps a 1 step)
            for col in range(row % 2, COL, 2):
                # topleft = 0,0 (x směrem do prava a y směrem dolu )
                pygame.draw.rect(win, BOARD_WHITE, (row*SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Metoda vykreslí hrací kameny a hrací pole => hrací plochu
    def Draw(self, win):
        self.DrawSquares(win)
        for row in range(ROW):
            for col in range(COL):
                stone = self.GameBoard[row][col]
                if stone != 0:
                    stone.Draw(win)
    #Metoda pro pohyb
    #1. pohyb kamene v listu + 2. update

    def Movement(self, stone, row, col):
        # Prohození pozic hodnot; nemusíme vytvářet temp
        self.GameBoard[stone.row][stone.col], self.GameBoard[row][col] = self.GameBoard[row][col], self.GameBoard[stone.row][stone.col]
        stone.Move(row, col)

        #Kontrola zda jsme na pozici kdy se stone může stát queen + update hodnot self.black_queens a self.white_queens
        if row == ROW - 1 or row == 0:  # Jestliže jsme na pozici 0 nebo 7 tak jsme na konci či začátku hrací plohcy => kámen se stává dámou
            queen = PieceQueen.fromPiece(stone)
            self.GameBoard[queen.row][queen.col] = queen
            if queen.color == BLACK:
                self.black_queens += 1
            elif queen.color == WHITE:
                self.white_queens += 1

    #Metoda pro stone aby jsme jej mohli předat do movement v main()
    def GetStone(self, row, col):
        return self.GameBoard[row][col]

    #Odstranění hracího kamene jesliže byl přeskočen
    def Remove(self, stones):
        for stone in stones:
            self.GameBoard[stone.row][stone.col] = 0
            #Pokud byl hrací kámen přeskočen jest odstraněn ze počtu celkových hracích kamenů
            if stone != 0:
                if stone.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    #Metoda vrátí barvu vítěze, prozatím takto jeduduché ve
    def Winner(self):
        if self.white_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return WHITE

        return None  # Pokud nikdo nevyhraje tak None

#Algoritmus který vezme hrací kámen a pro daný hrací kámen určí všechny možné správné pohyby které může vykonat
    #Musíme zkontrolovat zda se jedná ho černý nebo bílý hrací kámen
    # - Jestliže je to černý kámen tak se můžeme hýbat pouze směrem dolů
    # - Jestliže to je bílí kámen tak se můžeme hýbat pouze směrem nahoru
    #Jestliže na diaogáne je protihráčům kámen => můžeme ho přeskočit? => jak pro levý či prahý pohyb
    # - Kontrola dále po diagonále zda můžeme přeskočit
    #Doublejump rule => Jestliže jsme přeskočili kontrola zda můžeme po diagonále znovu přeskočit

    def GetCorrectMoves(self, stone):
        self.forcedMoves = {}
        moves = {}  # ukládát pozice (row, col)
        turnStays = {}  # Saves the same number of items as moves, decides if the turn should change/stay

        if isinstance(stone, PieceNormal):
            pieceMoves, turnStaysPiece = self._GetPieceMoves(stone)
            turnStays.update({"turn": turnStaysPiece})
            moves.update(pieceMoves)

        if isinstance(stone, PieceQueen):
            queenMoves, turnStaysQueen = self._GetQueenMoves(stone)
            turnStays.update({"turn": turnStaysQueen})
            moves.update(queenMoves)

        if self.forcedMoves == {}:
            return moves, turnStays
        else:
            return self.forcedMoves, turnStays

    def _isInbounds(self, pos):
        return pos[0] >= 0 and pos[0] < ROW and pos[1] >= 0 and pos[1] < COL

    def _isGamePiece(self, tile):
        return isinstance(tile, PieceNormal) or isinstance(tile, PieceQueen)

    def _GetPieceMoves(self, stone):
        moves = {}
        turnStays = False

        # Starts movement left up
        if stone.color == WHITE:
            left = -1
            up = -1

        # Starts movement left down
        if stone.color == BLACK:
            left = -1
            up = 1

        # For each axis
        for k in range(2):
            # Get all the tiles on the axis

            # Movement for right up
            if stone.color == WHITE and k == 1:
                left += 2

            # Movement for right down
            if stone.color == BLACK and k == 1:
                up += 2

            tiles = {}
            for i in range(1, 2):
                newRow = stone.row + up * i
                newCol = stone.col + left * i
                if self._isInbounds((newRow, newCol)):
                    tiles[(newRow, newCol)] = (self.GameBoard[newRow][newCol])
                else:
                    break

            idx = -1
            for tilePos, tile in tiles.items():
                idx += 1
                if self._isGamePiece(tile):
                    if tile.color != stone.color:
                        # enemy
                        if idx + 1 < len(tiles) and list(tiles.values())[idx + 1] == 0:
                            # Check if the tile behind enemy is empty
                            hop = list(tiles.keys())[idx + 1]
                            self.forcedMoves[hop] = [tile]
                            # IF there are more options, one of them might be false, but a later one will be true, ovverriding the false and letting you move even if you shouldnt
                            # Should fix itself with a tree
                            turnStays = self._CheckNextHop(hop, tile)
                            # print("checked", turnStays)
                            break
                        else:
                            # not empty
                            break
                    else:
                        # fren
                        break

                if tile == 0:
                    moves[tilePos] = []

        return moves, turnStays

    def _GetQueenMoves(self, stone):
        moves = {}
        left = -1
        up = -1
        turnStays = False

        # For each axis
        for k in range(4):
            # Get all the tiles on the axis
            tiles = {}
            for i in range(1, 8):
                newRow = stone.row + up * i
                newCol = stone.col + left * i
                if self._isInbounds((newRow, newCol)):
                    tiles[(newRow, newCol)] = (self.GameBoard[newRow][newCol])
                else:
                    break

            idx = -1
            for tilePos, tile in tiles.items():
                idx += 1
                if self._isGamePiece(tile):
                    if tile.color != stone.color:
                        # enemy
                        if idx + 1 < len(tiles) and list(tiles.values())[idx + 1] == 0:
                            # Check if the tile behind enemy is empty
                            hop = list(tiles.keys())[idx + 1]
                            self.forcedMoves[hop] = [tile]
                            # IF there are more options, one of them might be false, but a later one will be true, ovverriding the false and letting you move even if you shouldnt
                            # Should fix itself with a tree
                            turnStays = self._CheckNextHop(hop, tile)
                            # print("checked", turnStays)
                            break
                        else:
                            # not empty
                            break
                    else:
                        # fren
                        break

                if tile == 0:
                    moves[tilePos] = []

            if k == 1:
                up = -up
            left = -left

        return moves, turnStays

    def _CheckNextHop(self, positionToCheck, ignoredStone):
        # We can only get into this situation by jumping over a stone,
        # so we can safely ignore that one stone (no ugly loops)

        # Check if there is another stone around
        # if true, look behind it if there is a 0

        checkRow = positionToCheck[0]
        checkCol = positionToCheck[1]

        left = -1
        up = -1

        for k in range(4):
            # if True:

            tiles = {}
            for i in range(1, 3):
                newRow = checkRow + up * i
                newCol = checkCol + left * i
                if self._isInbounds((newRow, newCol)):
                    tiles[(newRow, newCol)] = (self.GameBoard[newRow][newCol])

            if k == 1:
                up = -up
            left = -left

            if len(tiles.values()) != 2:
                # Too short, we're at the edge
                continue

            if list(tiles.values())[0] == 0:
                # Empty tile next to positionToCheck
                continue

            if list(tiles.values())[0] is ignoredStone:
                continue

            # Safe to assume tile is occupied by a Stone
            # Check friendly stone
            if list(tiles.values())[0].color != ignoredStone.color:
                continue

            # Check behind it
            if list(tiles.values())[1] != 0:
                # Not empty, can't jump the piece
                continue

            # If we got here, we found a stone with an empty space behind
            return True
        return False

        #Methods for AI

        # Game board visualisation for reference
        # [[Stone(), 0, Stone()]
        # [0, Stone(), 0]
        # []]

    #Score for AI (better evaluate => better AI) => BLACK is AI, for now (perhaps make it a choise?)
    def evaluate(self):
        return self.black_left - self.white_left + (self.black_queens * 1.5 - self.white_queens * 1.5)
        #If AI can jump => AI must jump

    #Returns the number of stones of a specific colour
    def get_all_stones(self, color):
        stones = []
        for row in self.GameBoard:
            for stone in row:
                if stone != 0 and stone.color == color:
                    stones.append(stone)
        return stones

    @property
    def GameBoard(self):
        return self._GameBoard

    @GameBoard.setter
    def GameBoard(self, value):
        self._GameBoard = value

    @GameBoard.deleter
    def GameBoard(self):
        del self._GameBoard

    @staticmethod
    def NotationToCoordinates(notation):
        letters = [char for char in "abcdefghijklmnopqrstuvwxyz"]
        split = [c for c in notation]
        return [ROW - int(split[1]), letters.index(split[0])]

    @staticmethod
    def CoordinatesToNotation(row, col):
        letters = [char for char in "abcdefghijklmnopqrstuvwxyz"]
        return f"{letters[col]}{ROW - row}"

    @staticmethod
    def IsBlackTile(tile_notation):
        coordinates = GameBoard.NotationToCoordinates(tile_notation)
        row = coordinates[0]
        col = coordinates[1]
        if row % 2 == 0:  # Odd rows - black tiles are on odd cols
            if col % 2 == 1:
                return True
        else:  # Even rows - black tiles are on even cols
            if col % 2 == 0:
                return True
        return False
