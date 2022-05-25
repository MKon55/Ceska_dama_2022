# Hlavní část programu
# Pro pygame => pip install pygame

import pygame
from game.game_board import Game_board

#Importování modulu ze game
from game.stat_values import WIDTH, HEIGHT, SQUARE_SIZE
from game.file_manager import File_manager
from game.game_movement import Gameing

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dáma")  # Název hry

#Metoda která určit row, col pozice naší myši 
def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    game_runing = True
    gaming_time = pygame.time.Clock()  # Ať máme stálou rychlost hry, nemusí být
    #board = Game_board()
    game = Gameing(WIN)

    #Načítání a ukládání ze partie 
    #loaded_game = File_manager().read_file("savegame1")
    #print(loaded_game)
    #board.load_board(loaded_game)

    #File_manager().save_file(board.game_board, "savegame2")

    while game_runing:
        gaming_time.tick(FPS)

        #Win => ukončení hry, potom můžeme vylepšit 
        if  game.game_winner() != None:
            print("The mission, the nightmare... they are finally... over.")
            game_runing = False

        for event in pygame.event.get():
            # Event pro pygame => ukončení hry (button)
            if event.type == pygame.QUIT:
                game_runing = False

            if event.type == pygame.MOUSEBUTTONUP:  # Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos)
                game.select(row, col)
                #Testovací jednotka pro kliknuti.pohyb
                #board.movement(stone, 4, 3)
                
        #board.draw(WINDOW)
        #pygame.display.update()  # Pro update hracího pole když hrajeme hru
        game.update()

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
