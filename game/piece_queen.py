import pygame
from .game_piece import GamePiece
from .stat_values import SQUARE_SIZE, CROWN


class PieceQueen(GamePiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def Draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))  # Blit umožní vykreslení crown na hrací kámen + "matematika" pro vykreslení přímo do prostředí
