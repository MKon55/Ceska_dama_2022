import pygame


from game.screen_manager import WINDOW_WIDTH, WINDOW_HEIGHT, WIDTH, HEIGHT

pygame.font.init()
main_font = pygame.font.SysFont("calibri", 50)


class Button():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.text_render = main_font.render(self.text, True, "white")
        self.rect = self.text_render.get_rect(center=(self.x, self.y))
        self.rect = self.rect.inflate(20, 20)
        self.text_rect = self.text_render.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        rr = pygame.Rect(WIDTH, 0, WINDOW_WIDTH - WIDTH, WINDOW_HEIGHT)
        self.rect = self.rect.clamp(rr)
        pygame.draw.rect(screen, "red", rr)
        pygame.draw.rect(screen, "black", self.rect)
        screen.blit(self.text_render, self.rect)

    def click(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            print("Button Press!")

    def hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text_render = main_font.render(self.text, True, "green")
        else:
            self.text_render = main_font.render(self.text, True, "white")
