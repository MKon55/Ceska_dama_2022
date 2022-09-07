from game.stat_values import WHITE, WHITE_TEXT, BLACK_TEXT
from game.screen_manager import WIDTH, HEIGHT
import pygame


class TurnIndicator:
    def __init__(self):
        self.main_font = pygame.font.SysFont("calibri", 40)

    def draw(self, win, turn):
        playerTxt = str(WHITE_TEXT if turn == WHITE else BLACK_TEXT)
        text_render = self.main_font.render("Právě hraje:", True, (0, 0, 0))
        player_render = self.main_font.render(playerTxt, True, turn)
        rect = text_render.get_rect(center=(WIDTH + 140, HEIGHT / 2 - 100))
        prect = player_render.get_rect(topleft=rect.topright)
        win.blit(text_render, rect)
        win.blit(player_render, prect)
