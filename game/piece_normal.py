import pygame
import pygame.gfxdraw
from .game_piece import GamePiece
from .stat_values import SQUARE_SIZE


class PieceNormal(GamePiece):

    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def Draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.gfxdraw.aacircle(win, self.x, self.y, radius, self.color)
        pygame.gfxdraw.filled_circle(win, self.x, self.y, radius, self.color)
