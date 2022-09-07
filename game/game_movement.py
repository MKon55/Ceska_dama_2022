import pygame
import time
import random
from datetime import datetime

from .stat_values import BLACK, SQUARE_SIZE, WHITE, GREEN, SIDEBAR_BG, DEFAULT_COLOR_TURN, LAST_TURN, WHITE_TEXT, BLACK_TEXT
import AI_Minimax.algorithm
from game.screen_manager import WIDTH, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from game.turn_indicator import TurnIndicator
from game.game_over_text import GameOverText
from game.game_board import GameBoard
from game.button import Button
from game.tree import Tree


class Gameing:
    turn = DEFAULT_COLOR_TURN

    def __init__(self, win, aiPick=False):
        Gameing.turn = DEFAULT_COLOR_TURN
        self._StartCall()
        self._initUI()
        self.win = win
        self.gameOver = False
        self.aiColorPicking = aiPick

    def _initUI(self):
        self.saveBtn = Button(WIDTH + (WINDOW_WIDTH - WIDTH) / 2, HEIGHT / 2, "Uložit Hru", self.SaveButtonAction)
        self.backBtn = Button(WIDTH + (WINDOW_WIDTH - WIDTH) / 2, HEIGHT / 2 + 100, "Hlavní Menu", self.BackButtonAction)
        self.aiWhiteBtn = Button(WINDOW_WIDTH / 2 - 100, HEIGHT / 2, WHITE_TEXT, self.AiWhiteAction)
        self.aiBlackBtn = Button(WINDOW_WIDTH / 2 + 100, HEIGHT / 2, BLACK_TEXT, self.AiBlackAction)
        self.aiButtons = [self.aiWhiteBtn, self.aiBlackBtn]
        self.aiText = pygame.font.SysFont("calibri", 40).render("Za jakou barvu bude hrát AI?", True, (0, 0, 0))
        self.aiTextRect = self.aiText.get_rect(center=(WINDOW_WIDTH / 2, HEIGHT / 2 - 100))
        self.buttons = [self.saveBtn, self.backBtn]
        self.turnIndic = TurnIndicator()
        self.gameOverText = GameOverText()
        self.saveText = pygame.font.SysFont("calibri", 40).render("Hra uložena", True, (0, 0, 0))
        self.saveTextRect = self.saveText.get_rect(center=(WIDTH + 110, HEIGHT - 110))
        self.saveTextTimer = 0

    def _StartCall(self):
        self.selected_stone = None
        self.board = GameBoard()
        self.turn = Gameing.turn  # Tah začíná z pravidla bílí
        self.correct_moves = {}  # Ukaže možné správné pohyby pro daného hráče
        self.last_move = {}
        self.game_running = True  # Flag for main, doesnt actually control if game is running, that's main's job
        self._SetTree()

    def _SetTree(self):
        self.tree = Tree(self.board)
        self._GenerateTreeLevel()

    def LoadBoard(self, board):
        self.board.LoadBoard(board)

    # Update display, nyní jej nemusíme mít ve main.py
    def Update(self, mouse_pos):
        if self.aiColorPicking:
            self.win.fill(SIDEBAR_BG)
            for btn in self.aiButtons:
                btn.hover(mouse_pos)
                btn.draw(self.win)
            self.win.blit(self.aiText, self.aiTextRect)
            pygame.display.update()
            return

        self.board.Draw(self.win)

        sidebar = pygame.Rect(WIDTH, 0, WINDOW_WIDTH - WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.win, SIDEBAR_BG, sidebar)

        self.turnIndic.draw(self.win, self.turn)

        # Update all the buttons
        for btn in self.buttons:
            btn.hover(mouse_pos)
            btn.draw(self.win)

        # Save confirmation
        surface = pygame.Surface(self.saveTextRect.size)
        surface.fill(SIDEBAR_BG)
        surfaceRect = self.saveText.get_rect(topleft=(0, 0))
        surface.blit(self.saveText, surfaceRect)
        surface.set_alpha(self.saveTextTimer)
        self.saveTextTimer -= 4
        if self.saveTextTimer < 0:
            self.saveTextTimer = 0
        self.win.blit(surface, self.saveTextRect)

        self.DrawMoves(self.correct_moves, GREEN, 160)
        self.DrawMoves(self.last_move, LAST_TURN, 80)

        self.board.DrawPieces(self.win)

        if self.gameOver:
            self.gameOverText.draw(self.win, self.turn)

        pygame.display.update()

        # Tell main that the game should stop
        if not self.game_running:
            return False

    # Action for mouse release
    def Select(self, row, col, pos):
        # If we play against ai, we let the player choose the ai color before playing
        if self.aiColorPicking:
            for btn in self.aiButtons:
                btn.release()
                # run action for every button, end game if we get False back
                if btn.action(pos) is True:
                    self.aiColorPicking = False
            return None

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
            # Save last performed move
            last_move = {}
            last_move[self.selected_stone.pos] = []
            last_move[(row, col)] = []

            result, turnChange = self.tree.Move((row, col))

            # #Jestliže náš pohyb není validní tak pohyb nebude proveden a znovu zavoláme metodu Select
            self.selected_stone.selected = False  # Tell to stone it's not selected
            self.selected_stone = None  # Remove selected for Gameing
            self.tree.UnselectNode()  # Tell the tree to unselect
            self.correct_moves = {}  # Clear the moves when piece is deselected

            if result is False:  # Move failed
                self.Select(row, col, pos)  # Try selecting again
                return False
            elif result is True:
                self.last_move = last_move
                if turnChange:
                    self.ChangeTurn()
                self._GenerateTreeLevel()
                return True

        stone = self.board.GetStone(row, col)
        # Jestliže hrací kámen který jsme vybrali existuje a vybrali jsme SVOJI barvu
        if stone != 0 and stone.color == self.turn:
            self.selected_stone = stone
            stone.selected = True
            self.tree.SelectNode(self.board.GameBoard)
            self.correct_moves = self.tree.GetMovesForSelected()
            self.correct_moves[(stone.row, stone.col)] = []  # Shows which piece is selected
            return True  # Výběr a pohyb je správný -> vrátíme True

        return False  # Výběr a pohyb byl nesprávný -> vrátíme False

    # Mousedown action
    def ButtonClick(self, pos):
        for btn in self.aiButtons:
            btn.click(pos)
        for btn in self.buttons:
            btn.click(pos)

    # Metoda která nám vykreslí možné správné pohyby
    def DrawMoves(self, moves, color, alpha):
        for move in moves:
            row, col = move
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(alpha)
            s.fill(color)
            self.win.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Check if mouse position (x, y) is outside of the playable area
    def _IsOutsideOfGameboard(self, pos):
        return (pos[0] < 0 or pos[1] < 0 or pos[0] > WIDTH or pos[1] > HEIGHT)

    # Metoda pro změnu tahu
    def ChangeTurn(self):
        self.correct_moves = {}  # Odstraní zelené možnosti po našem tahu
        self.turn = BLACK if self.turn == WHITE else WHITE
        Gameing.turn = self.turn

    def SetTurn(self, color):
        self.turn = color
        Gameing.turn = self.turn
        self._SetTree()

    def _GenerateTreeLevel(self):
        generateResult = self.tree.GenerateLevel(self.board, self.turn)
        if generateResult is not None:
            self.gameOver = True

    # Button functions
    def SaveButtonAction(self):
        from game.file_manager import FileManager
        stamp = "dama-save-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        FileManager.SaveFile(self.board.GameBoard, stamp)
        self.saveTextTimer = 255

    def BackButtonAction(self):
        return False

    def AiWhiteAction(self):
        AI_Minimax.algorithm.ChangeAIColor(WHITE)
        return True

    def AiBlackAction(self):
        AI_Minimax.algorithm.ChangeAIColor(BLACK)
        return True

    # Methods for AI
    # Method for getting board object
    def get_board(self):
        return self.board

    # Method returns new board after AI move => updates game with new board object
    def AI_move(self, board):
        selectedPos, move = self.tree.GetMoveFromBoard(board.GameBoard)
        if move is None:
            return

        # Wait some time to give the effect of ai "thinking"
        time.sleep(random.uniform(0.4, 1.5))

        row, col = selectedPos
        self.Select(row, col, (0, 0))
        self.Update((0, 0))

        row, col = move
        self.Select(row, col, (0, 0))
        self.Update((0, 0))
