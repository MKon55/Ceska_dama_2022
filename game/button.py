import pygame

from game.stat_values import BUTTON_BG, BUTTON_TEXT, BUTTON_HOVER, BUTTON_PRESS, BUTTON_HOVER_TEXT, BUTTON_PRESS_TEXT
from game.screen_manager import WINDOW_WIDTH, WINDOW_HEIGHT, WIDTH

pygame.font.init()
main_font = pygame.font.SysFont("calibri", 40)


class Button():
    # x, y = position
    # text = display text
    # func = function that will be executed during action()
    def __init__(self, x, y, text, func):
        self.x = x
        self.y = y
        self.text = text
        self.text_render = main_font.render(self.text, True, BUTTON_TEXT)
        self.rect = self.text_render.get_rect(center=(self.x, self.y))
        padding = 40  # Padding around the text
        self.rect = self.rect.inflate(padding, padding)
        self.text_rect = self.text_render.get_rect(center=(self.x, self.y))
        self.hovering = False
        self.clicking = False
        self.func = func

    def draw(self, screen):
        if self.clicking:
            pygame.draw.rect(screen, BUTTON_PRESS, self.rect, border_radius=2)
        elif self.hovering:
            pygame.draw.rect(screen, BUTTON_HOVER, self.rect, border_radius=2)
        else:
            pygame.draw.rect(screen, BUTTON_BG, self.rect, border_radius=2)
        screen.blit(self.text_render, self.text_rect)

    def isMouseInside(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)

    # Call on mouseDown event
    def click(self, pos):
        if self.isMouseInside(pos):
            self.text_render = main_font.render(self.text, True, BUTTON_PRESS_TEXT)
            self.clicking = True
        else:
            self.text_render = main_font.render(self.text, True, BUTTON_TEXT)
            self.clicking = False

    # Call on mouseUp event
    def release(self):
        self.text_render = main_font.render(self.text, True, BUTTON_TEXT)
        self.clicking = False

    # Call on update
    def hover(self, position):
        if self.clicking:
            return
        if self.isMouseInside(position):
            self.text_render = main_font.render(self.text, True, BUTTON_HOVER_TEXT)
            self.hovering = True
        else:
            self.text_render = main_font.render(self.text, True, BUTTON_TEXT)
            self.hovering = False

    # Call on mouseUp event
    def action(self, pos):
        if self.isMouseInside(pos):
            return self.func()
