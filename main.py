# Hlavní část programu
# Pro pygame => pip install pygame
import sys
import pygame
import pygame_menu

# Importování modulu ze game
from game.screen_manager import WINDOW_WIDTH, WINDOW_HEIGHT
from game.stat_values import SQUARE_SIZE, MENUTHEME, BLACK
import game.file_picker
from game.file_manager import FileManager
from game.game_movement import Gameing
from AI_Minimax.algorithm import minimax

FPS = 60
pygame.init()
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dáma")  # Název hry


# Metoda která určit row, col pozice naší myši
def GetMousePos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


# Start the game with 2 players
def StartPlayers():
    Main()


# Start the game against ai
def StartAi():
    Main(AI=True)


# Start the game from a .csv file
def LoadGame(AI=False):
    pathToFile = game.file_picker.FilePicker()
    if pathToFile is None:
        return
    loadedGame, turn = FileManager().ReadFile(pathToFile)
    Main(loadedGame, turn, AI=AI)


# Load the game and play against ai
def LoadGameAI():
    LoadGame(AI=True)


# Main menu (opens first)
def MainMenu():
    menu = pygame_menu.Menu('Dáma', WINDOW_WIDTH, WINDOW_HEIGHT, theme=MENUTHEME)

    menu.add.button('Hrát ve dvou', StartPlayers)
    menu.add.button('Hrát proti AI', StartAi)
    menu.add.button('Nahrát hru', LoadGame)
    menu.add.button('Nahrát hru (AI)', LoadGameAI)
    menu.add.button('Ukončit', pygame_menu.events.EXIT)

    menu.mainloop(WIN)


# Main game loop
def Main(loadedGame=None, turn=None, AI=False):
    game_running = True
    gaming_time = pygame.time.Clock()  # Ať máme stálou rychlost hry, nemusí být
    game = Gameing(WIN)

    # Load a game if we get a board
    if loadedGame is not None:
        game.LoadBoard(loadedGame)
        game.SetTurn(turn)

    while game_running:
        gaming_time.tick(FPS)

        # Method calls minimax algorith on colour
        if AI is True and game.turn == BLACK:
            value, new_board = minimax(game.get_board(), 4, BLACK, game)  # depth = 3, bigger number better ai but longer calculations, value, new board => tuple
            game.AI_move(new_board)

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # Event pro pygame => ukončení hry (button)
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.ButtonClick(pos)

            if event.type == pygame.MOUSEBUTTONUP:  # Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat
                row, col = GetMousePos(pos)
                game.Select(row, col, pos)

        if game.Update(pos) is False:
            MainMenu()

    pygame.quit()  # ukončení window pro hru
    sys.exit()


MainMenu()
