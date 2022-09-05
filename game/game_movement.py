import pygame
from datetime import datetime

from .stat_values import BLACK, SQUARE_SIZE, WHITE, GREEN, SIDEBAR_BG, DEFAULT_COLOR_TURN, LAST_TURN
from game.screen_manager import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from game.turn_indicator import TurnIndicator
from game.game_over_text import GameOverText
from game.game_board import GameBoard
from game.button import Button
from game.tree import Tree


class Gameing:
    turn = DEFAULT_COLOR_TURN

    def __init__(self, win):
        Gameing.turn = DEFAULT_COLOR_TURN
        self._StartCall()
        self.win = win
        self.saveBtn = Button(WIDTH + 110, HEIGHT - 50, "Uložit Hru", self.SaveButtonAction)
        self.backBtn = Button(WIDTH + 140 + self.saveBtn.rect.width, HEIGHT - 50, "Hlavní Menu", self.BackButtonAction)
        self.buttons = [self.saveBtn, self.backBtn]
        self.turnIndic = TurnIndicator()
        self.gameOver = False
        self.gameOverText = GameOverText()

    # Update display, nyní jej nemusíme mít ve main.py
    def Update(self, mouse_pos):
        if self.selecting:
            # print(self.tree._PrintBoard(self.board.GameBoard))
            result = self.tree.GenerateLevel(self.board, self.turn)
            self.selecting = False
            self.moving = False
            if result is not None:
                self.gameOver = True

        self.board.Draw(self.win)

        sidebar = pygame.Rect(WIDTH, 0, WINDOW_WIDTH - WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.win, SIDEBAR_BG, sidebar)

        self.turnIndic.draw(self.win, self.turn)

        # Update all the buttons
        for btn in self.buttons:
            btn.hover(mouse_pos)
            btn.draw(self.win)

        self.DrawMoves(self.correct_moves, GREEN, 160)
        self.DrawMoves(self.last_move, LAST_TURN, 80)

        self.board.DrawPieces(self.win)

        if self.gameOver:
            self.gameOverText.draw(self.win, self.turn)

        pygame.display.update()

        # Tell main that the game should stop
        if not self.game_running:
            return False

    def _StartCall(self):
        self.selected_stone = None
        self.board = GameBoard()
        self.turn = Gameing.turn  # Tah začíná z pravidla bílí
        self.correct_moves = {}  # Ukaže možné správné pohyby pro daného hráče
        self.last_move = {}
        self.game_running = True  # Flag for main, doesnt actually control if game is running, that's main's job
        self._SetTree()

    def LoadBoard(self, board):
        self.board.LoadBoard(board)
        self._SetTree()

    def _SetTree(self):
        self.tree = Tree(self.board)
        self.selecting = True
        self.moving = False

    def GameWinner(self):
        return self.board.Winner()

    # Metoda pro vyběr hracího kamene -> určí row a col -> hýbne s hracím kamenem dle našeho výběru
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
            last_move = {}
            last_move[self.selected_stone.pos] = []
            last_move[(row, col)] = []
            result, turnChange = self.tree.Move((row, col))
            # #Jestliže náš pohyb není validní tak pohyb nebude proveden a znovu zavoláme metodu Select
            self.selected_stone.selected = False
            self.selected_stone = None
            self.tree.UnselectNode()
            self.moving = False
            self.correct_moves = {}  # Clear the moves when piece is deselected
            if result is False:
                self.Select(row, col, pos)
                return False
            elif result is True:
                self.last_move = last_move
                self.selecting = True
                if turnChange:
                    self.ChangeTurn()
                return True

        stone = self.board.GetStone(row, col)
        # Jestliže hrací kámen který jsme vybrali existuje a vybrali jsme SVOJI barvu
        if stone != 0 and stone.color == self.turn:
            self.selected_stone = stone
            stone.selected = True
            self.tree.SelectNode(self.board.GameBoard)
            self.moving = True
            self.correct_moves = self.tree.GetMovesForSelected()
            self.correct_moves[(stone.row, stone.col)] = []  # Shows which piece is selected
            return True  # Výběr a pohyb je správný -> vrátíme True

        return False  # Výběr a pohyb byl nesprávný -> vrátíme False

    def ButtonClick(self, pos):
        for btn in self.buttons:
            btn.click(pos)

    # Check if mouse position (x, y) is outside of the playable area
    def _IsOutsideOfGameboard(self, pos):
        return (pos[0] < 0 or pos[1] < 0 or pos[0] > WIDTH or pos[1] > HEIGHT)

    # Metoda která nám vykreslí možné správné pohyby
    def DrawMoves(self, moves, color, alpha):
        for move in moves:
            row, col = move
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(alpha)
            s.fill(color)
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

    # Methods for AI
    # Method for getting board object
    def get_board(self):
        return self.board

    # Method returns new board after AI move => updates game with new board object
    def AI_move(self, board):
        selectedPos, move = self.tree.GetMoveFromBoard(board.GameBoard)
        if move is None:
            # raise Exception("AI move invalid")
            return
        # import time
        row, col = selectedPos
        # print("clicking", row, col)
        self.Select(row, col, (0, 0))
        self.Update((0, 0))
        # time.sleep(1)
        row, col = move
        # print("clicking", row, col)
        self.Select(row, col, (0, 0))
        self.Update((0, 0))
