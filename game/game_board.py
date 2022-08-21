# Vytváří hrací plochu pro dámu
# Pohyb hracích kamenů

import pygame
# musí být . jinak neví že .py je ve stejné složce
from .stat_values import BOARD_BLACK, BOARD_WHITE, SQUARE_SIZE, ROW, COL, BLACK, WHITE
from .stone import Stone

class Game_board:
    def __init__(self):
        self._game_board = []
        self.black_left = 12
        self.white_left = 12
        self.black_queens = 0
        self.white_queens = 0
        self.create_game_board()

    # Metoda vytvoří herní plochu
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
            
    # Metoda vykreslí čtverce ve kterých budou hrací kameny
    def draw_squares(self, win):
        win.fill(BOARD_BLACK)
        for row in range(ROW):
            # step 2 pro správné vykreslení (střídání 2 steps a 1 step)
            for col in range(row % 2, COL, 2):
                # topleft = 0,0 (x směrem do prava a y směrem dolu )
                pygame.draw.rect(win, BOARD_WHITE, (row*SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Metoda vykreslí hrací kameny a hrací pole => hrací plochu
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROW):
            for col in range(COL):
                stone = self.game_board[row][col]
                if stone != 0:
                    stone.draw(win)
                               
    #Metoda pro pohyb
    #1. pohyb kamene v listu + 2. update 
    def movement(self, stone, row, col):
        # Prohození pozic hodnot; nemusíme vytvářet temp
        self.game_board[stone.row][stone.col], self.game_board[row][col] = self.game_board[row][col], self.game_board[stone.row][stone.col]
        stone.move(row, col)
        
        #Kontrola zda jsme na pozici kdy se stone může stát queen + update hodnot self.black_queens a self.white_queens 
        if row == ROW - 1 or row == 0: #Jestliže jsme na pozici 0 nebo 7 tak jsme na konci či začátku hrací plohcy => kámen se stává dámou 
            stone.make_queen()
            if stone.color == BLACK and not stone.queen:
                self.black_queens += 1
            elif stone.color == WHITE and not stone.queen: 
                self.white_queens += 1     
       
    #Metoda pro stone aby jsme jej mohli předat do movement v main()         
    def get_stone(self, row, col):
        return self.game_board[row][col]
    
    #Odstranění hracího kamene jesliže byl přeskočen 
    def remove(self, stones):
        for stone in stones:
            self.game_board[stone.row][stone.col] = 0
            #Pokud byl hrací kámen přeskočen jest odstraněn ze počtu celkových hracích kamenů
            if stone != 0:
                if stone.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1
                    
    #Metoda vrátí barvu vítěze, prozatím takto jeduduché 
    def winner(self):
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
    
    def get_correct_moves(self, stone):
        moves = {} #ukládát pozice (row, col)
        left = stone.col - 1
        right = stone.col + 1
        row = stone.row
        
        #Kontrola barvy + PROZATÍM nechávám dámu ve stejném pohybu musíme ještě implementovat specifický pohyb dámy => pohyb po celé diagonále + dáma má přednost!!
        if stone.color == WHITE or stone.queen:
            #Jsme White pohybujeme se nahoru, Jak "hodně nahoru se koukáme"
            moves.update(self._movement_left(row -1, max(row-3, -1), -1, stone.color, left))
            moves.update(self._movement_right(row -1, max(row-3, -1), -1, stone.color, right))
            
        if stone.color == BLACK or stone.queen:
            #Nyní se pohybujeme dolů tudíž +1, min()
            moves.update(self._movement_left(row +1, min(row+3, ROW), 1, stone.color, left))
            moves.update(self._movement_right(row +1, min(row+3, ROW), 1, stone.color, right))
            
        return moves
            
    #Pohyb po levé diagonále     
    def _movement_left(self, start, stop, step, color, left, skipped=[]): #step určí jakým směrem se pohybujeme, skip určí zda jsme nějakou přeskočili
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0: #Jestliže koumáme již mimo hrací pole 
                break
            
            #Traversování do levé strany
            current = self.game_board[r][left]
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
                        row = max(r-3,-1) #Fix for white double jump 0 -> -1
                    else:
                        row = min(r+3, ROW)
                    
                    #Rekalkulace jestliže jsme skočili a nyní můžeme double or triple
                    moves.update(self._movement_left(r+step, row, step, color, left-1, skipped = last))
                    moves.update(self._movement_right(r+step, row, step, color, left+1, skipped = last))
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
    def _movement_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COL: #Jestliže koumáme již mimo hrací pole 
                break
            
            #Traversování do pravé strany
            current_move = self.game_board[r][right]
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
                        row = max(r-3,-1)
                    else:
                        row = min(r+3, ROW)
                    
                    #Rekalkulace jestliže jsme skočili a nyní můžeme double or triple
                    moves.update(self._movement_left(r+step, row, step, color, right-1, skipped = last))
                    moves.update(self._movement_right(r+step, row, step, color, right+1, skipped = last))
                break #Pro jistotu aby byl pohyb zastaven po double or triple 
                    
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
        for row in self.game_board:
            for stone in row:
                if stone != 0 and stone.color == color:
                    stones.append(stone)
        return stones
            
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
