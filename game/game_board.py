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

    def SetBoard(self, board):
        self._GameBoard = []
        for row in range(ROW):
            self._GameBoard.append([])
            for col in range(COL):
                self._GameBoard[row].append(board[row][col])

    # Metoda pro načtení hrací plochy
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

    # Vyčištení hrací plochy
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

    def DrawPieces(self, win):
        for row in range(ROW):
            for col in range(COL):
                stone = self.GameBoard[row][col]
                if stone != 0:
                    stone.Draw(win)

    # Metoda pro stone aby jsme jej mohli předat do movement v main()
    def GetStone(self, row, col):
        return self.GameBoard[row][col]

    # Returns all availible moves for the stone
    def GetCorrectMoves(self, stone):
        self.forcedMoves = {}
        self.turnStays = {}
        moves = {}  # ukládát pozice (row, col)
        turnStays = {}  # Saves the same number of items as moves, decides if the turn should change/stay

        # Calls method for possible moves + update
        pieceMoves = self._GetPieceMoves(stone)
        turnStays.update(self.turnStays)
        moves.update(pieceMoves)

        # Gets us forced moves according to the rules
        if self.forcedMoves == {}:
            return moves, turnStays, False
        else:
            return self.forcedMoves, turnStays, True

    # Check for game piece
    def _isInbounds(self, pos):
        return pos[0] >= 0 and pos[0] < ROW and pos[1] >= 0 and pos[1] < COL

    def _isGamePiece(self, tile):
        return isinstance(tile, PieceNormal) or isinstance(tile, PieceQueen)

    # Method gets us all possible moves for selected game piece
    def _GetPieceMoves(self, stone):
        moves = {}
        # Start for White Normal Piece and Queen Piece
        x = 2
        y = 3
        left = -1
        up = -1

        # Starts movement for black piece
        if stone.color == BLACK and isinstance(stone, PieceNormal):
            left = -1
            up = 1

        if isinstance(stone, PieceQueen):
            x = 4
            y = 8

        # For each axis, get all the tiles on the axis
        for k in range(x):

            # Movement for right up
            if k == 1 and isinstance(stone, PieceNormal):
                left = -left

            tiles = {}
            for i in range(1, y):
                newRow = stone.row + up * i
                newCol = stone.col + left * i
                if self._isInbounds((newRow, newCol)):
                    tiles[(newRow, newCol)] = (self.GameBoard[newRow][newCol])
                else:
                    break

            # This part of the code is the same
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
                            if isinstance(stone, PieceNormal):
                                self.turnStays[hop] = self._CheckNextHop(hop, tile, False, stone.color)
                            if isinstance(stone, PieceQueen):
                                self.turnStays[hop] = self._CheckNextHop(hop, tile, True)
                            break
                        else:
                            # not empty
                            break
                    else:
                        # fren
                        break

                # This part is a mess but it works
                if tile == 0 and idx < 1 and isinstance(stone, PieceNormal):
                    moves[tilePos] = []

                if tile == 0 and isinstance(stone, PieceQueen):
                    moves[tilePos] = []

            if k == 1 and isinstance(stone, PieceQueen):
                up = -up

            if isinstance(stone, PieceQueen):
                left = -left

        return moves

    def _CheckNextHop(self, positionToCheck, ignoredStone, isQueen, color=None):
        # We can only get into this situation by jumping over a stone,
        # so we can safely ignore that one stone (no ugly loops)

        # Check if there is another stone around
        # if true, look behind it if there is a 0

        checkRow, checkCol = positionToCheck

        if isQueen:
            left = -1
            up = -1
            checkRange = range(4)
        else:
            left = -1
            checkRange = range(2)
            if color == WHITE:
                up = -1
            elif color == BLACK:
                up = 1
            else:
                raise Exception("Missing color")

        for k in checkRange:
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

    # Methods for AI
    # Score for AI (better evaluate => better AI) => BLACK is AI, for now (perhaps make it a choise?)
    def _GetAIValues(self):
        black_left, white_left, black_queens, white_queens = 0, 0, 0, 0
        for row in range(ROW):
            for col in range(COL):
                p = self.GameBoard[row][col]
                if p != 0:
                    if p.color == WHITE:
                        if isinstance(p, PieceQueen):
                            white_queens += 1
                        else:
                            white_left += 1
                    else:
                        if isinstance(p, PieceQueen):
                            black_queens += 1
                        else:
                            black_left += 1
        return black_left, white_left, black_queens, white_queens

    def evaluate(self):
        black_left, white_left, black_queens, white_queens = self._GetAIValues()
        return black_left - white_left + (black_queens * 1.5 - white_queens * 1.5)
        # If AI can jump => AI must jump

    # Returns the number of stones of a specific colour
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
