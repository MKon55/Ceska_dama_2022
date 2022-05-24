# Hlavní část programu
# Pro pygame => pip install pygame

import pygame

#Importování modulu ze game
from game.stat_values import WIDTH, HEIGHT
from game.game_board import Game_board
from game.file_manager import File_manager

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dáma")  # Název hry


def main():
    game = True
    gaming_time = pygame.time.Clock()  # Ať máme stálou rychlost hry, nemusí být
    board = Game_board()

    loaded_game = File_manager().read_file("savegame1")
    print(loaded_game)
    board.load_board(loaded_game)

    File_manager().save_file(board.game_board, "savegame2")

    while game:
        gaming_time.tick(FPS)

        for event in pygame.event.get():
            # Event pro pygame => ukončení hry (button)
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONUP:  # Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat
                pass

        board.draw(WINDOW)
        pygame.display.update()  # Pro update hracího pole když hrajeme hru

    pygame.quit()  # ukončení window pro hru


main()

#vytvoření "předgui" pro načtení ze souboru .csv nebo začátek nové partie
#   Něco jako main menu ve hře
#   Vedle hracího pole ještě počet herních kamenů, počet dám a jaký hráč je na tahu (převděpodobně na pravé straně okna pygame)
#       Viz Fišerova práce na přednášce
#Potřeba tedy vytvořit načtení pozic do hracího pole ze .csv souboru (pokusím se implementovat ale mám problém s pochopením)
#   Zároveň uložit kdykoliv partii do .csv souboru (cyklus který vezmu nynější pozici hracích kamenu a toho kdo je na tahu)
#   Specifické pojmenování a rozložení dat musí být spleněno jinak exception!!
#Začátek nové partie již můžeme začít pomocí již daného kodu
