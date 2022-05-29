# Vytváří hrací plochu pro dámu
# Pohyb hracích kamenů

import pygame
# musí být . jinak neví že .py je ve stejné složce
from .stat_values import BOARD_BLACK, BOARD_WHITE, SQUARE_SIZE, ROW, COL, BLACK, WHITE
from .stone import Stone

class GameBoard:
    def __init__(self):
        self._GameBoard = []
        self.black_left = self.white_left = 12
        self.black_queens = self.white_queens = 0
        self.CreateGameBoard()

    # Metoda vytvoří herní plochu
    def CreateGameBoard(self):
        for row in range(ROW):
            self._GameBoard.append([])  # List pro každou řadu
            for col in range(COL):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self._GameBoard[row].append(
                            Stone(row, col, BLACK))
                    elif row > 4:
                        self._GameBoard[row].append(
                            Stone(row, col, WHITE))
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
                self._GameBoard[row][col] = Stone(row, col, BLACK, False)
            elif color_and_queen == "bb":
                self._GameBoard[row][col] = Stone(row, col, BLACK, True)
            elif color_and_queen == "w":
                self._GameBoard[row][col] = Stone(row, col, WHITE, False)
            elif color_and_queen == "ww":
                self._GameBoard[row][col] = Stone(row, col, WHITE, True)

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
        if row == ROW - 1 or row == 0: #Jestliže jsme na pozici 0 nebo 7 tak jsme na konci či začátku hrací plohcy => kámen se stává dámou 
            stone.MakeQueen()
            if stone.color == BLACK:
                self.black_queens += 1
            else: 
                self.white_queens += 1               
       
    #Metoda pro stone aby jsme jej mohli předat do M v main()         
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
        
        return None #Pokud nikdo nevyhraje tak None
 
#Algoritmus který vezme hrací kámen a pro daný hrací kámen určí všechny možné správné pohyby které může vykonat 
    #Musíme zkontrolovat zda se jedná ho černý nebo bílý hrací kámen 
    # - Jestliže je to černý kámen tak se můžeme hýbat pouze směrem dolů 
    # - Jestliže to je bílí kámen tak se můžeme hýbat pouze směrem nahoru 
    #Jestliže na diaogáne je protihráčům kámen => můžeme ho přeskočit? => jak pro levý či prahý pohyb 
    # - Kontrola dále po diagonále zda můžeme přeskočit 
    #Doublejump rule => Jestliže jsme přeskočili kontrola zda můžeme po diagonále znovu přeskočit
    
    def GetCorrectMoves(self, stone):
        moves = {} #ukládát pozice (row, col)
        left = stone.col - 1
        right = stone.col + 1
        row = stone.row
        
        #Kontrola barvy + PROZATÍM nechávám dámu ve stejném pohybu musíme ještě implementovat specifický pohyb dámy => pohyb po celé diagonále + dáma má přednost!!
        if stone.color == WHITE or stone.queen:
            #Jsme White pohybujeme se nahoru, Jak "hodně nahoru se koukáme"
            moves.update(self._MovementLeft(row -1, max(row-3, -1), -1, stone.color, left))
            moves.update(self._MovementRight(row -1, max(row-3, -1), -1, stone.color, right))
            
        if stone.color == BLACK or stone.queen:
            #Nyní se pohybujeme dolů tudíž +1, min()
            moves.update(self._MovementLeft(row +1, min(row+3, ROW), 1, stone.color, left))
            moves.update(self._MovementRight(row +1, min(row+3, ROW), 1, stone.color, right))
            
        return moves
            
    #Pohyb po levé diagonále     
    def _MovementLeft(self, start, stop, step, color, left, skipped=[]): #step určí jakým směrem se pohybujeme, skip určí zda jsme nějakou přeskočili
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0: #Jestliže koumáme již mimo hrací pole 
                break
            
            #Traversování do levé strany
            current = self.GameBoard[r][left]
            #Pokud == 0 tak jsme našli prazdné pole do kterého se můžeme hýbnout 
            if current == 0:
                if skipped and not last:
                    break #Jestliže jsme přeskočili a již nemůžeme nic jiného přeskočit tak už se nemůžeme hýbat
                elif skipped:
                    moves[(r, left)] = last + skipped #Toto určuje potom co jsme přeskočili jaké kameny máme odstranit ze hry
                #Pukud splněnuje předchozí tak jej můžeme přeskočit 
                else:
                    moves[(r, left)] = last
                 
                #Kontrola zda můžeme double or triple
                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3, ROW)
                    
                    #Rekalkulace jestliže jsme skočili a nyní můžeme double or triple
                    moves.update(self._MovementLeft(r+step, row, step, color, left-1, skipped = last))
                    moves.update(self._MovementRight(r+step, row, step, color, left+1, skipped = last))
                break #Pro jistotu aby byl pohyb zastaven po double or triple 
                    
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
            if right >= COL: #Jestliže koumáme již mimo hrací pole 
                break
            
            #Traversování do pravé strany
            current_move = self.GameBoard[r][right]
            #Pokud == 0 tak jsme našli prazdné pole do kterého se můžeme hýbnout 
            if current_move == 0:
                if skipped and not last:
                    break #Jestliže jsme přeskočili a již nemůžeme nic jiného přeskočit tak už se nemůžeme hýbat
                elif skipped:
                    moves[(r, right)] = last + skipped #Toto určuje potom co jsme přeskočili jaké kameny máme odstranit ze hry
                #Pukud splněnuje předchozí tak jej můžeme přeskočit 
                else:
                    moves[(r, right)] = last
                 
                #Kontrola zda můžeme double or triple
                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3, ROW)
                    
                    #Rekalkulace jestliže jsme skočili a nyní můžeme double or triple
                    moves.update(self._MovementLeft(r+step, row, step, color, right-1, skipped = last))
                    moves.update(self._MovementRight(r+step, row, step, color, right+1, skipped = last))
                break #Pro jistotu aby byl pohyb zastaven po double or triple 
                    
            #Pokud poli je hrací kámen který je stejné barvy tak se tam nemůžeme hýbnout 
            elif current_move.color == color:
                break
            #Pokud to není naší barvy tak je to protihráčovo kámen a můžeme se hýbnout S TÍM  že předpokládáme že za ní je prázdné pole 
            else:
                last = [current_move] 
                    
            right += 1
            
        return moves
            
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
