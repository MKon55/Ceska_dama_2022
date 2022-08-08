# Hlavní část programu
# Pro pygame => pip install pygame
import sys
import pygame

import pygame_menu

# Importování modulu ze game
from game.screen_manager import WIDTH, HEIGHT
from game.stat_values import SQUARE_SIZE, MENUTHEME
import game.file_picker
from game.file_manager import FileManager
from game.game_movement import Gameing

FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
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
    Main()


# Start the game from a .csv file
def LoadGame():
    pathToFile = game.file_picker.FilePicker()
    if pathToFile is None:
        return
    loadedGame, turn = FileManager().ReadFile(pathToFile)
    Main(loadedGame, turn)


# Main menu (opens first)
def MainMenu():
    menu = pygame_menu.Menu('Dáma', WIDTH, HEIGHT, theme=MENUTHEME)

    menu.add.button('Hrát ve dvou', StartPlayers)
    menu.add.button('Hrát proti AI', StartAi)
    menu.add.button('Nahrát hru', LoadGame)
    menu.add.button('Ukončit', pygame_menu.events.EXIT)

    menu.mainloop(WIN)


# Main game loop
def Main(loadedGame=None, turn=None):
    game_running = True
    gaming_time = pygame.time.Clock()  # Ať máme stálou rychlost hry, nemusí být
    game = Gameing(WIN)

    # Load a game if we get a board
    if loadedGame is not None:
        game.board.LoadBoard(loadedGame)
        game.SetTurn(turn)

    FileManager.SaveFile(game.board.GameBoard, "savegame2")

    while game_running:
        gaming_time.tick(FPS)

        #Win => ukončení hry, potom můžeme vylepšit
        if game.GameWinner() != None:
            print("The mission, the nightmare... they are finally... over.")
            game_running = False

        for event in pygame.event.get():
            # Event pro pygame => ukončení hry (button)
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONUP:  # Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat
                pos = pygame.mouse.get_pos()
                row, col = GetMousePos(pos)
                game.Select(row, col)

        game.Update()

    pygame.quit()  # ukončení window pro hru
    sys.exit()


MainMenu()

#vytvoření "předgui" pro načtení ze souboru .csv nebo začátek nové partie
#   Něco jako Main menu ve hře
#   Vedle hracího pole ještě počet herních kamenů, počet dám a jaký hráč je na tahu (převděpodobně na pravé straně okna pygame)
#       Viz Fišerova práce na přednášce
#Potřeba tedy vytvořit načtení pozic do hracího pole ze .csv souboru (pokusím se implementovat ale mám problém s pochopením)
#   Zároveň uložit kdykoliv partii do .csv souboru (cyklus který vezmu nynější pozici hracích kamenu a toho kdo je na tahu)
#   Specifické pojmenování a rozložení dat musí být spleněno jinak exception!!
#Začátek nové partie již můžeme začít pomocí již daného kodu
