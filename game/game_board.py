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
        self.blacklistStones = []
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
        self.blacklistStones = []
        moves = {}  # ukládát pozice (row, col)
        row = stone.row
        col = stone.col
        left = col - 1
        right = col + 1

        #Kontrola barvy + PROZATÍM nechávám dámu ve stejném pohybu musíme ještě implementovat specifický pohyb dámy => pohyb po celé diagonále + dáma má přednost!!
        if stone.color == WHITE and isinstance(stone, PieceNormal):
            #Jsme White pohybujeme se nahoru, Jak "hodně nahoru se koukáme"
            moves.update(self._MovementLeft(row - 1, max(row-3, -1), -1, stone.color, left))
            moves.update(self._MovementRight(row - 1, max(row-3, -1), -1, stone.color, right))

        if stone.color == BLACK and isinstance(stone, PieceNormal):
            #Nyní se pohybujeme dolů tudíž +1, min()
            moves.update(self._MovementLeft(row + 1, min(row+3, ROW), 1, stone.color, left))
            moves.update(self._MovementRight(row + 1, min(row+3, ROW), 1, stone.color, right))

        if isinstance(stone, PieceQueen):
            #left = col - 1
            #right = col + 1

            #moves.update(self._QueenMovement(stone))
            moves.update(self._GetQueenMoves(stone))

            # #Movement LEFT -> UP
            # moves.update(self._MovementLeft(row - 1, max(row-3, -1), -1, stone.color, left))
            # #Movement LEFT -> DOWN
            # moves.update(self._MovementLeft(row + 1, min(row+3, ROW), 1, stone.color, left))
            # #Movement RIGHT -> UP
            # moves.update(self._MovementRight(row - 1, max(row-3, -1), -1, stone.color, right))
            # #Movement RIGHT -> DOWN
            # moves.update(self._MovementRight(row + 1, min(row+3, ROW), 1, stone.color, right))

        # print(self.forcedMoves)
        if self.forcedMoves == {}:
            return moves
        else:
            return self.forcedMoves

    def _isInbounds(self, pos):
        return pos[0] >= 0 and pos[0] < ROW and pos[1] >= 0 and pos[1] < COL

    def _isGamePiece(self, tile):
        return isinstance(tile, PieceNormal) or isinstance(tile, PieceQueen)

    def _GetQueenMoves(self, stone):
        moves = {}
        left = -1
        up = -1

        tiles = {}
        for i in range(1, 8):
            newRow = stone.row + up * i
            newCol = stone.col + left * i
            if self._isInbounds((newRow, newCol)):
                tiles[(newRow, newCol)] = (self.GameBoard[newRow][newCol])

        idx = -1
        for tilePos, tile in tiles.items():
            idx += 1
            if self._isGamePiece(tile):
                print("stone")
                if tile.color != stone.color:
                    # enemy
                    if idx + 1 < len(tiles) and list(tiles.values())[idx + 1] == 0:
                        print("free")
                        # empty behind enemy
                        # forced move
                        # check if any other jumpable enemy is around -> turn should stay
                        # else, turn changes
                        self.forcedMoves[list(tiles)[idx + 1]] = tile
                    else:
                        # not empty
                        break
                else:
                    # fren
                    break

            if tile == 0:
                moves[tilePos] = []

        print(self.forcedMoves)
        print(moves)
        return moves

    # TODO: Optimize this, so we only check one of the diagonals
    # returns isMoveValid(boolean), jumpedEnemy(None|Stone)
    def _isValidQueenMove(self, selectedPos, selectedColor, move):
        row = selectedPos[0]
        col = selectedPos[1]
        color = selectedColor

        leftRight = -1
        topBottom = -1

        # Loop 4 times for the 4 axis
        for k in range(4):
            enemyStone = None

            potentialMove = (row + topBottom, col + leftRight)

            distanceFromSelected = 1
            while self._isInbounds(potentialMove):
                GameBoardTile = self.GameBoard[potentialMove[0]][potentialMove[1]]
                if GameBoardTile != 0:
                    # occupied tile
                    if color != GameBoardTile.color:
                        # Opposite colors
                        if enemyStone is None:
                            enemyStone = GameBoardTile
                        else:
                            break
                    else:
                        # Same color, cant over
                        break

                # We found location of "move"
                if potentialMove == move:
                    if GameBoardTile == 0:
                        # Empty destination
                        return True, enemyStone
                    else:
                        return False, enemyStone

                distanceFromSelected += 1
                potentialMove = (row + topBottom * distanceFromSelected, col + leftRight * distanceFromSelected)

            if k % 2 == 1:
                leftRight = -1
            else:
                leftRight = 1
            if k >= 1:
                topBottom = 1
        return False, None

    def _checkSecondaryJump(self, startPos, color):
        noRecursion = True

        a = -2
        b = -2

        for i in range(4):
            Pos = (startPos[0] + a, startPos[1] + b)
            Valid, Stone = self._isValidQueenMove(startPos, color, Pos)

            if Valid:
                if Stone is not None:  # and Stone not in self.blacklistStones:
                    # Go again
                    self.blacklistStones.append(Stone)
                    self.forcedMoves[Pos] = []
                    #self._checkSecondaryJump(Pos, color)
                    # noRecursion = False

            b = -b
            if i == 1:
                a = -a

        if noRecursion:
            self.forcedMoves[startPos] = []

    def _QueenMovement(self, stone):
        # go through each diagonal
        # if its valid move and we are jumping an enemy, check secondaryJump recursively
        moves = {}

        leftRight = -1
        topBottom = -1

        # Loop 4 times for the 4 axis
        for k in range(4):

            distanceFromSelected = 0
            potentialMove = (stone.row + leftRight * distanceFromSelected, stone.col + topBottom * distanceFromSelected)

            while self._isInbounds(potentialMove):
                isValid, jumpedStone = self._isValidQueenMove(stone.pos, stone.color, potentialMove)
                # if(jumpedStone is not None):
                #     print(potentialMove, isValid, jumpedStone.pos)
                # else:
                #     print(potentialMove, isValid, jumpedStone)
                if isValid and jumpedStone is not None:
                    # CODE RED: The move will jump over an enemy
                    # check secondaryJump
                    # if there is no secondaryJump, add this move to forcedMoves
                    # potentialMove is the new starting location we check fromPiece
                    self.blacklistStones.append(jumpedStone)
                    # self._checkSecondaryJump(potentialMove, stone.color)
                    self.forcedMoves[potentialMove] = []
                    break

                elif isValid:
                    moves[potentialMove] = []

                distanceFromSelected += 1
                potentialMove = (stone.row + leftRight * distanceFromSelected, stone.col + topBottom * distanceFromSelected)

            if k % 2 == 1:
                leftRight = -1
            else:
                leftRight = 1
            if k >= 1:
                topBottom = 1

        return moves

    #Pohyb po levé diagonále
    def _MovementLeft(self, start, stop, step, color, left, skipped=[]):  # step určí jakým směrem se pohybujeme, skip určí zda jsme nějakou přeskočili
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:  # Jestliže koumáme již mimo hrací pole
                break

            #Traversování do levé strany
            current = self.GameBoard[r][left]
            #Pokud == 0 tak jsme našli prazdné pole do kterého se můžeme hýbnout
            if current == 0:
                if skipped and not last:
                    break  # Jestliže jsme přeskočili a již nemůžeme nic jiného přeskočit tak už se nemůžeme hýbat
                elif skipped:
                    moves[(r, left)] = last + skipped  # Toto určuje potom co jsme přeskočili jaké kameny máme odstranit ze hry
                #Pukud splněnuje předchozí tak jej můžeme přeskočit
                else:
                    moves[(r, left)] = last

                #Kontrola zda můžeme double or triple
                if last:
                    if step == -1:
                        row = max(r-3, -1)  # Fix for white double jump 0 -> -1
                    else:
                        row = min(r+3, ROW)

                    #Rekalkulace jestliže jsme skočili a nyní můžeme double or triple
                    moves.update(self._MovementLeft(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._MovementRight(r+step, row, step, color, left+1, skipped=last))
                break  # Pro jistotu aby byl pohyb zastaven po double or triple

            #Pokud poli je hrací kámen který je stejné barvy tak se tam nemůžeme hýbnout
            elif current.color == color:
                break
            #Pokud to není naší barvy tak je to protihráčovo kámen a můžeme se hýbnout S TÍM  že předpokládáme že za ní je prázdné pole
            else:
                last = [current]

            left -= 1

        return moves

    #Pohyb po pravé diagonále
    def _MovementRight(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COL:  # Jestliže koumáme již mimo hrací pole
                break

            #Traversování do pravé strany
            current_move = self.GameBoard[r][right]
            #Pokud == 0 tak jsme našli prazdné pole do kterého se můžeme hýbnout
            if current_move == 0:
                if skipped and not last:
                    break  # Jestliže jsme přeskočili a již nemůžeme nic jiného přeskočit tak už se nemůžeme hýbat
                elif skipped:
                    moves[(r, right)] = last + skipped  # Toto určuje potom co jsme přeskočili jaké kameny máme odstranit ze hry
                #Pukud splněnuje předchozí tak jej můžeme přeskočit
                else:
                    moves[(r, right)] = last

                #Kontrola zda můžeme double or triple
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROW)

                    #Rekalkulace jestliže jsme skočili a nyní můžeme double or triple
                    moves.update(self._MovementLeft(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._MovementRight(r+step, row, step, color, right+1, skipped=last))
                break  # Pro jistotu aby byl pohyb zastaven po double or triple

            #Pokud poli je hrací kámen který je stejné barvy tak se tam nemůžeme hýbnout
            elif current_move.color == color:
                break
            #Pokud to není naší barvy tak je to protihráčovo kámen a můžeme se hýbnout S TÍM  že předpokládáme že za ní je prázdné pole
            else:
                last = [current_move]

            right += 1

        return moves

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
