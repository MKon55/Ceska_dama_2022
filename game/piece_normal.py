import pygame
from .game_piece import GamePiece
from .stat_values import SQUARE_SIZE


class PieceNormal(GamePiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def Draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
