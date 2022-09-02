from game.stat_values import WHITE, BLACK, WHITE_TEXT, BLACK_TEXT
from game.screen_manager import WIDTH, HEIGHT
import pygame


class GameOverText:

    def __init__(self):
        self.main_font = pygame.font.SysFont("calibri", 100)

    def draw(self, win, turn):
        x = WIDTH / 2
        y = HEIGHT / 2
        bgCol = WHITE if turn == BLACK else BLACK
        winner = WHITE_TEXT if turn == BLACK else BLACK_TEXT
        text = f"Konec! Vítěz: {winner}"
        text_render = self.main_font.render(text, True, (255, 255, 255))
        rect = text_render.get_rect(center=(x, y))
        padding = 100  # Padding around the text
        rect = rect.inflate(padding, padding)
        text_rect = text_render.get_rect(center=(x, y))
        pygame.draw.rect(win, bgCol, rect, border_radius=2)
        win.blit(text_render, text_rect)
