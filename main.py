# Hlavní část programu
# Pro pygame => pip install pygame

import sys
import pygame
import pygame_menu
from pathlib import Path

#Importování modulu ze hra
from hra.hodnoty import WIDTH, HEIGHT
from hra.hraci_plocha import Hraci_plocha
from hra.file_manager import File_manager

FPS = 60

pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dáma")  # Název hry


def start_the_game():
    main()


def main_menu():  # Main menu (opens first)
    mytheme = pygame_menu.Theme(background_color=(204, 255, 224),
                                title_background_color=(25, 200, 25),
                                title_font_shadow=False,
                                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                                title_font_size=150,
                                title_font_color=(14, 14, 14),
                                title_offset=(WIDTH / 2 - 200, 50),
                                widget_padding=25,
                                title_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
                                widget_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
                                selection_color=(15, 200, 15)
                                )

    menu = pygame_menu.Menu('Dáma', WIDTH, HEIGHT, theme=mytheme)

    menu.add.button('Hrát ve dvou', start_the_game)
    menu.add.button('Hrát proti AI', start_the_game)
    menu.add.button('Nahrát hru', start_the_game)
    menu.add.button('Ukončit', pygame_menu.events.EXIT)

    menu.mainloop(WINDOW)


def main():  # Main game loop
    hra = True
    cas_hry = pygame.time.Clock()  # Ať máme stálou rychlost hry, nemusí být
    plocha = Hraci_plocha()

    loaded_game = File_manager().read_file("savegame1")
    print(loaded_game)
    plocha.load_board(loaded_game)

    File_manager().save_file(plocha.herni_plocha, "savegame2")

    while hra:
        cas_hry.tick(FPS)

        for event in pygame.event.get():
            # Event pro pygame => ukončení hry (button)
            if event.type == pygame.QUIT:
                hra = False

            if event.type == pygame.MOUSEBUTTONUP:  # Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat
                pass

        plocha.draw(WINDOW)
        pygame.display.update()  # Pro update hracího pole když hrajeme hru

    pygame.quit()  # ukončení window pro hru
    sys.exit()


#main()
main_menu()

#vytvoření "předgui" pro načtení ze souboru .csv nebo začátek nové partie
#   Něco jako main menu ve hře
#   Vedle hracího pole ještě počet herních kamenů, počet dám a jaký hráč je na tahu (převděpodobně na pravé straně okna pygame)
#       Viz Fišerova práce na přednášce
#Potřeba tedy vytvořit načtení pozic do hracího pole ze .csv souboru (pokusím se implementovat ale mám problém s pochopením)
#   Zároveň uložit kdykoliv partii do .csv souboru (cyklus který vezmu nynější pozici hracích kamenu a toho kdo je na tahu)
#   Specifické pojmenování a rozložení dat musí být spleněno jinak exception!!
#Začátek nové partie již můžeme začít pomocí již daného kodu
